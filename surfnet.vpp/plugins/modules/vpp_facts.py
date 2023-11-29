# -*- coding: utf-8 -*-
#
# Copyright 2023 SURF B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

DOCUMENTATION = r"""
module: vpp_facts
short_description: Gather facts from VPP
description: Gather facts from VPP with predefined default sets
version_added: 0.0.1
author: SURF B.V. (@surfnet)

options:
    operation:
      description: The operation mode this module is running as.
      default: get
      choices:
       - get
    all:
      description: Gather all known facts
      type: bool
      default: false
    filter:
      description: Show a specific filter
      type: str
      default: ""
    sorting:
      description: How do sort facts
      type: str
      choices:
        - asc
        - desc
        - ""
      default: ""
"""

EXAMPLES = r"""
- name: Gather all VPP facts
  surfnet.vpp.vpp_facts:
    all: true
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy
from typing import Union, List

__metaclass__ = type

from ansible_collections.surfnet.vpp.plugins.module_utils.vpp_common import (
    connect,
    disconnect,
    get_version,
    to_vpp,
    format_fact,
    api_available,
)
from ansible_collections.surfnet.vpp.plugins.module_utils.const import (
    VPPModuleMethods,
    GatherDetails,
)


def run_module():
    module_args = dict(
        operation=dict(
            type="str", default=VPPModuleMethods.GET, choices=[VPPModuleMethods.GET]
        ),
        all=dict(type="bool", required=False, default=False),
        filter=dict(type="str", required=False, default=""),
        sorting=dict(type="str", default="", choices=["", "asc", "desc"]),
    )

    result = dict(changed=False, message="")

    ansible_facts = dict()

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    def _compile_filter(input_filter: Union[List, str]) -> List:
        """Formats a filter (user input) into something we can understand"""
        # Check if we have this in our list of queries
        filtered_list = list
        if isinstance(input_filter, str):
            if input_filter in GatherDetails.ALL:
                filtered_list = [input_filter]
        elif isinstance(input_filter, list):
            for flt in input_filter:
                if flt in GatherDetails.ALL:
                    filtered_list.append(flt)
        return filtered_list

    if not api_available:
        module.fail_json(
            "VPP API could not be loaded. Please make sure vpp-papi is installed."
        )

    conn = connect()

    vpp_version = get_version(connection=conn)

    # Find what stats we are going to grab
    if module.params["all"]:
        fact_filter = GatherDetails.ALL
    elif module.params["filter"] == "":
        fact_filter = GatherDetails.COMMON
    else:
        fact_filter = _compile_filter(module.params["filter"])

    fact_gatherer = {}
    for apicmd in fact_filter:
        cmd_result = to_vpp(conn, str(apicmd))
        if cmd_result["retval"] == 0:
            fact_name = f"vpp_{apicmd}"
            fact_gatherer.update({fact_name: format_fact(cmd_result["value"], apicmd)})

    unsorted_facts = fact_gatherer
    sorted_facts = dict

    # Sort the facts if we need to
    if module.params["sorting"] == "asc":
        unsorted_facts = deepcopy(fact_gatherer)
        sorted_facts = dict(sorted(unsorted_facts.items()))
    elif module.params["sorting"] == "desc":
        unsorted_facts = deepcopy(fact_gatherer)
        sorted_facts = dict(sorted(unsorted_facts.items(), reverse=True))

    ansible_facts = unsorted_facts if module.params["sorting"] == "" else sorted_facts

    ret = disconnect(connection=conn)

    module.exit_json(**result, **ansible_facts)


def main():
    run_module()


if __name__ == "__main__":
    main()
