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
module: vpp_vhostuser
short_description: Manage VPP vhost-user interfaces
description: Manage VPP vhost-user interface one at at time
version_added: 0.0.2
author: SURF B.V. (@surfnet)

options:
    state:
      description: The operation mode this module is running as.
      default: set
      choices:
       - present
       - absent
      type: str
    if_idx:
      description: The interface number (sw_if_index) used by VPP for this interface
      type: int
    is_server:
      description: Should this vhost-user interface be server (true) or client (false)
      type: bool
      default: false
    sock_filename:
      description: Filename of the socket this interface communicates with
      type: str
      required: true
    tag:
      description: Freeform tag to add to vhost-user interface
      type: str
"""

EXAMPLES = r"""
- name: Ensure vhost-user interface exists
  surfnet.vpp.vpp_vhostuser:
    sock_filename: example.sock
    tag: Hello world
"""

RETURN = r""" # """

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.surfnet.vpp.plugins.module_utils.vpp_common import (
    connect,
    disconnect,
    get_version,
    get_error,
    get_vhost_if,
    api_available,
)
from ansible_collections.surfnet.vpp.plugins.module_utils.const import (
    VPPModuleMethods,
    VPP_SOCKET_DIR,
)
import os

__metaclass__ = type


def run_module():
    module_args = dict(
        state=dict(
            type="str",
            default=VPPModuleMethods.PRESENT,
            choices=[VPPModuleMethods.ABSENT, VPPModuleMethods.PRESENT],
        ),
        if_idx=dict(type="int", required=False, default=None),
        is_server=dict(type="bool", required=False, default=False),
        sock_filename=dict(type="str", required=True),
        tag=dict(type="str", required=False),
    )

    result = dict(changed=False, message="")

    ansible_facts = dict()

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    if not api_available:
        module.fail_json(
            "VPP API could not be loaded. Please make sure vpp-papi is installed."
        )

    conn = connect()

    vpp_version = get_version(connection=conn)

    # Create / change
    if module.params.get("state") == VPPModuleMethods.PRESENT:

        existing_if = None
        opt_sock_full_filename = str

        if os.path.exists(VPP_SOCKET_DIR):
            opt_sock_full_filename = os.path.join(
                VPP_SOCKET_DIR, module.params.get("sock_filename")
            )
        else:
            module.fail_json(
                msg=f"Socket directory {VPP_SOCKET_DIR} does not exist or cannot access",
                **result,
            )

        if module.params.get("if_idx") is not None:
            opt_if_idx = int(module.params.get("if_idx"))
        else:
            opt_if_idx = None
        opt_is_server = bool(module.params.get("is_server"))
        opt_tag = str(module.params.get("tag"))
        opt_sock_filename = str(module.params.get("sock_filename"))

        # See if the interface already exists, since we do not know for sure
        if not opt_if_idx and opt_sock_filename:
            existing_if = get_vhost_if(
                connection=conn, sock_filename=opt_sock_full_filename
            )
        elif opt_if_idx:
            existing_if = get_vhost_if(connection=conn, if_idx=opt_if_idx)

        # New interface requested
        if not existing_if:

            if vpp_version[0] > 22:
                interface = conn.api.create_vhost_user_if_v2(
                    is_server=opt_is_server,
                    sock_filename=opt_sock_full_filename,
                    tag=opt_tag,
                )

            else:
                interface = conn.api.create_vhost_user_if(
                    is_server=opt_is_server,
                    sock_filename=opt_sock_full_filename,
                    tag=opt_tag,
                )

            if interface and interface.retval != 0:
                name, errid, text = get_error(interface.retval)
                module.fail_json(
                    msg=f"Could not create vhost-user interface {opt_sock_filename}:{text} ({errid})",
                    **result,
                )
            else:
                result["changed"] = True
                result["message"] = (
                    f"Succesfully created vhost-user interface at {opt_sock_filename}, "
                    f"interface index is {interface.sw_if_index}"
                )

        # Modification of existing interface requested
        else:
            sw_if_idx = existing_if.sw_if_index

            # Only do something if there is something to change
            if (
                opt_is_server != existing_if.is_server
                or opt_sock_filename != existing_if.sock_filename
            ):

                if vpp_version[0] > 22:
                    res = conn.api.modify_vhost_user_if_v2(
                        sw_if_index=sw_if_idx,
                        is_server=opt_is_server,
                        sock_filename=opt_sock_full_filename,
                    )
                else:
                    res = conn.api.modify_vhost_user_if_v2(
                        sw_if_index=sw_if_idx,
                        is_server=opt_is_server,
                        sock_filename=opt_sock_full_filename,
                    )

                if res and res.retval != 0:
                    name, errid, text = get_error(res.retval)
                    module.fail_json(
                        msg=f"Could not modify vhost-user interface {opt_sock_filename}:{text} ({errid})",
                        **result,
                    )
                else:
                    result["changed"] = True
                    result[
                        "message"
                    ] = f"Succesfully modified vhost-user interface at {opt_sock_filename}"
    # Delete
    elif module.params.get("state") == VPPModuleMethods.ABSENT:

        if module.params.get("if_idx") is not None:
            opt_if_idx = int(module.params.get("if_idx"))
        else:
            opt_if_idx = None
        opt_sock_filename = str(module.params.get("sock_filename"))

        if os.path.exists(VPP_SOCKET_DIR):
            opt_sock_full_filename = os.path.join(
                VPP_SOCKET_DIR, module.params.get("sock_filename")
            )
        else:
            module.fail_json(
                msg=f"Socket directory {VPP_SOCKET_DIR} does not exist or cannot access",
                **result,
            )

        # If we have the socket, make sure it matches the ifidx we got, so we are predictable
        if_by_filename = None
        if_by_idx = None

        if opt_sock_filename:
            if_by_filename = get_vhost_if(
                connection=conn, sock_filename=opt_sock_full_filename
            )
        if opt_if_idx:
            if_by_idx = get_vhost_if(connection=conn, if_idx=opt_if_idx)

        if (
            if_by_idx is not None
            and if_by_filename is not None
            and if_by_idx == if_by_filename
        ):
            res = conn.api.delete_vhost_user_if(sw_if_index=opt_if_idx)

        elif if_by_idx is not None:
            res = conn.api.delete_vhost_user_if(sw_if_index=opt_if_idx)

        elif if_by_filename is not None:
            res = conn.api.delete_vhost_user_if(sw_if_index=if_by_filename.sw_if_index)

        else:
            res = None

        if res and res.retval != 0:
            name, errid, text = get_error(res.retval)
            module.fail_json(
                msg=f"Could not delete vhost-user interface at {if_by_idx.sock_filename} ({if_by_idx.sw_if_index}):"
                f" {text} ({errid})",
                **result,
            )
        elif res:
            result["changed"] = True
            result["message"] = "Succesfully deleted vhost-user interface"
    disconnect(connection=conn)
    module.exit_json(**result, **ansible_facts)


def main():
    run_module()


if __name__ == "__main__":
    main()
