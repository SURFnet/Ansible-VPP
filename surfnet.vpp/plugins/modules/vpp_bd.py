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
module: vpp_bd
short_description: Manage VPP broadcast domains
description: Manage VPP broadcast domains one domain at a time
version_added: 0.0.1
author: SURF B.V. (@surfnet)

options:
    state:
      description: The operation mode this module is running as.
      default: present
      choices:
       - present
       - absent
      type: str
    bd:
      description: The number of the broadcast domain we are influencing
      type: int
    flood:
      description: Should the bd support flooding
      type: bool
      default: true
    uu_flood:
      description: Should the bd support unicast flooding
      type: bool
      default: true
    learn:
      description: Should the bd support MAC learning
      type: bool
      default: true
    bd_tag:
      description: Freeform tag to add to bd
      type: str
"""

EXAMPLES = r"""
- name: Ensure bridge domain exists
  surfnet.vpp.vpp_bd:
    bd: 1
    bd_tag: Hello world
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.surfnet.vpp.plugins.module_utils.vpp_common import (
    connect,
    disconnect,
    get_version,
    get_error,
    api_available,
)
from ansible_collections.surfnet.vpp.plugins.module_utils.const import (
    VPPModuleMethods,
)

__metaclass__ = type


def run_module():
    module_args = dict(
        state=dict(
            type="str",
            default=VPPModuleMethods.PRESENT,
            choices=[VPPModuleMethods.PRESENT, VPPModuleMethods.ABSENT],
        ),
        bd=dict(type="int", required=False, default=None),
        flood=dict(type="bool", required=False, default=True),
        uu_flood=dict(type="bool", required=False, default=True),
        learn=dict(type="bool", required=False, default=True),
        bd_tag=dict(type="str", required=False),
    )

    result = dict(changed=False, message="")

    ansible_facts = dict()

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not api_available:
        module.fail_json(
            "VPP API could not be loaded. Please make sure vpp-papi is installed."
        )

    conn = connect()

    vpp_version = get_version(connection=conn)

    bd_raw = conn.api.bridge_domain_dump()

    if module.params.get("state") == VPPModuleMethods.PRESENT:

        has_changes = False
        bd_desired_options = {
            "bd_id": module.params.get("bd"),
            "flood": module.params.get("flood"),
            "uu_flood": module.params.get("uu_flood"),
            "forward": module.params.get("forward"),
            "learn": module.params.get("learn"),
            "arp_term": module.params.get("arp_term"),
            "bd_tag": module.params.get("bd_tag"),
        }

        # Convert passed options to dict, call bridge create/update afterward
        bd_call_args = {}
        for bd_option in bd_desired_options.keys():
            if bd_desired_options[bd_option] and bd_option != "bd_tag":
                bd_call_args[bd_option] = int(bd_desired_options[bd_option])
            elif bd_desired_options[bd_option] and bd_option == "bd_tag":
                bd_call_args[bd_option] = str(bd_desired_options[bd_option])
        bd_call_args["is_add"] = 1
        vpp_repl = False

        # Check if we have a fixed bridge domain id (not mandatory in v2 API call)
        if bd_desired_options["bd_id"]:
            bd = bd_desired_options["bd_id"]
            bd_info = {}
            for ent in bd_raw:
                if int(ent.bd_id) == int(bd):
                    bd_info = ent
            if bd_info:
                result["message"] = f"Bridge domain {bd} already exists. Not changing"
                module.exit_json(**result, **ansible_facts)
                # TODO: Fix handling of adjustments of existing bridge domains
                # Existing BD, figure out if anything has changed
                # curr_bd_config = bd_info._asdict()
                #
                # Look for changed value for existing option
                # for curr_bd_opt in curr_bd_config.keys():
                #    if ( curr_bd_opt in bd_desired_options and
                #         curr_bd_config[curr_bd_opt] != bd_desired_options[curr_bd_opt]):
                #        has_changes = True
                # Look for newly added option that was not defined
                # for desired_bd_opt in bd_desired_options.keys():
                #    if desired_bd_opt not in curr_bd_config:
                #        has_changes = True
                #
                # Handle any changes in bridge domain config
                # if has_changes:
                #    bridge_flags = BRIDGE_API_FLAGS.BRIDGE_API_FLAG_NONE
                #    for opt in bd_desired_options.keys():
                #        if bd_desired_options[opt]:
                #            if opt == "flood":
                #                bridge_flags += BRIDGE_API_FLAGS.BRIDGE_API_FLAG_FLOOD
                #            elif opt == "uu_flood":
                #                bridge_flags += (
                #                    BRIDGE_API_FLAGS.BRIDGE_API_FLAG_UU_FLOOD
                #                )
                #            elif opt == "forward":
                #                bridge_flags += BRIDGE_API_FLAGS.BRIDGE_API_FLAG_FWD
                #            elif opt == "learn":
                #                bridge_flags += BRIDGE_API_FLAGS.BRIDGE_API_FLAG_LEARN
                #            elif opt == "arp_term":
                #                bridge_flags += (
                #                    BRIDGE_API_FLAGS.BRIDGE_API_FLAG_ARP_TERM
                #                )
                #    if not module.check_mode:
                #        vpp_repl = conn.api.bridge_flags(
                #            bd_id=bd, is_set=True, flags=bridge_flags
                #        )
                # else:
                #    result["message"] = f"No changes needed for bridge domain {bd}"
            # New BD with ID set
            else:
                has_changes = True
                if not module.check_mode:
                    if vpp_version[0] > 22:
                        vpp_repl = conn.api.bridge_domain_add_del_v2(**bd_call_args)
                    else:
                        vpp_repl = conn.api.bridge_domain_add_del(**bd_call_args)
        else:
            # New BD
            has_changes = True
            if not module.check_mode:
                if vpp_version[0] > 22:
                    vpp_repl = conn.api.bridge_domain_add_del_v2(**bd_call_args)

                else:
                    vpp_repl = conn.api.bridge_domain_add_del(**bd_call_args)

        if not module.check_mode:
            if vpp_repl and vpp_repl.retval != 0:
                name, errid, text = get_error(vpp_repl.retval)
                module.fail_json(
                    msg=f"Could not perform action on bridge_domain {module.params.get('bd')}: "
                    f"{text} ({errid})",
                    **result,
                )
            else:
                if has_changes:
                    result["changed"] = True
                result[
                    "message"
                ] = f"Bridge domain {bd_desired_options['bd_id']} configured successfully"
        elif has_changes:
            result["changed"] = True

    elif module.params.get("state") == VPPModuleMethods.ABSENT:
        has_changes = False
        bd_id = module.params.get("bd")

        if bd_id:
            for entry in bd_raw:
                if int(entry.bd_id) == int(bd_id):
                    # We have something to delete
                    has_changes = True
                    if not module.check_mode:
                        if vpp_version[0] > 22:
                            vpp_repl = conn.api.bridge_domain_add_del_v2(
                                bd_id=bd_id, is_add=False
                            )
                        else:
                            vpp_repl = conn.api.bridge_domain_add_del(
                                bd_id=bd_id, is_add=False
                            )

            if not module.check_mode and has_changes:
                if vpp_repl and vpp_repl.retval != 0:
                    name, errid, text = get_error(vpp_repl.retval)
                    module.fail_json(
                        msg=f"Could not delete bridge domain {bd_id}: {text} ({errid})"
                    )
                else:
                    result["changed"] = True
                    result[
                        "message"
                    ] = f"Bridge domain {bd_id} has been deleted successfully"

    module.exit_json(**result, **ansible_facts)

    disconnect(connection=conn)


def main():
    run_module()


if __name__ == "__main__":
    main()
