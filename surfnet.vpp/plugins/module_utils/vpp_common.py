# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import fnmatch
from typing import List, Union, Tuple, Any, Callable, cast, Dict

try:
    from vpp_papi import VPPApiClient
except ImportError:
    VPPApiClient = None
from .const import VPP_DEFAULT_DIR, VPPErrors, FactFormats
from ansible.module_utils.errors import AnsibleValidationError
from ansible.module_utils.six.moves.collections_abc import Iterable


def connect(definitions: List = None) -> Union[VPPApiClient, bool]:
    """
    Connect to the VPP API

    :param definitions: List of API definitions
    :return: VPPApiClient instance
    :rtype: VPPApiClient
    """
    if not definitions:
        definitions = []
        for root, dirnames, filenames in os.walk(VPP_DEFAULT_DIR):
            for filename in fnmatch.filter(filenames, "*.api.json"):
                definitions.append(os.path.join(root, filename))

    client = VPPApiClient(apifiles=definitions)
    r = client.connect("python-ansible-vpp")
    if r == 0:
        return client
    else:
        return False


def disconnect(connection: VPPApiClient) -> int:
    """
    Disconnect from the VPP Api
    :param connection:
    :return: result from disconnect call
    """

    return connection.disconnect()


def api_available() -> bool:
    if VPPApiClient:
        return True
    else:
        return False


def get_version(connection: VPPApiClient) -> Tuple[int, int, bool]:
    """Return the 'semantic' version components of a VPP version

    :param connection: VPPApiClient instance that holds an active connection
    :return: Tuple with major, minor and remainder
    :rtype: Tuple
    """

    # version string is in the form yy.mm{stuff}
    version_string = connection.api.show_version().version
    yy = int(version_string[:2])
    mm = int(version_string[3:5])
    plus = len(version_string[5:]) != 0

    return yy, mm, plus


def get_error(errno: int) -> Tuple[str, int, str]:
    """Turn an errorcode into something a human can deal with
    :param errno: integer for the error
    :return: Tuple consisting of: Programmatic name, error id, human readable text
    """

    err = next(err for err in VPPErrors.ERRORS if errno in err)

    return err[0], err[1], err[2]


def to_vpp(connection: VPPApiClient, funcname: str, *args: Any, **kwargs: Any) -> Dict:
    """Send a call to VPP"""

    reply = {
        "error": str,
        "retval": int,
        "value": str,
    }

    try:
        func_call = cast(Callable, getattr(connection.api, funcname))
    except AttributeError:
        try:
            func_call = cast(Callable, getattr(connection, funcname))
        except AttributeError:
            raise AnsibleValidationError

    try:
        fc = func_call(*args, **kwargs)
    except IOError as e:
        pass

    if getattr(fc, "retval", 0) != 0:

        reply[
            "error"
        ] = f"Failed VPP call to {funcname}({' '.join(str(e) for e in args)}) ({kwargs})"
        reply["retval"] = getattr(fc, "retval")
        reply["value"] = fc

        return reply

    reply["retval"] = 0
    reply["value"] = fc
    return reply


def get_vhost_if(
    connection: VPPApiClient, sock_filename: str = None, if_idx: int = None
) -> Union[None, Any]:
    """
    Fetch details for a specified vhost-user interface
    :param connection: Reference to the connection
    :param sock_filename: socket file to look up
    :param if_idx: interface idx to look up
    :return: The fetched object or None if not found
    """

    vhost_table = connection.api.sw_interface_vhost_user_dump()
    vhost_if = None

    try:
        if sock_filename:
            vhost_if = next(
                intf for intf in vhost_table if intf.sock_filename == sock_filename
            )
        elif if_idx:
            vhost_if = next(intf for intf in vhost_table if intf.sw_if_index == if_idx)
        return vhost_if
    except StopIteration:
        return None


def add_tag_to_interface(connection: VPPApiClient.api, interface_id, value):
    """
    Add administrative tag to interface

    :param connection: Reference to connection
    :param interface_id: Interface ID to tag
    :param value: Value of tag to set
    :return: True if success, False if not
    """

    tag = connection.sw_interface_tag_add_del(
        sw_if_index=interface_id, tag=value, is_add=1
    )
    return bool(tag.retval == 0)


def todict(obj, limit=sys.getrecursionlimit(), classkey=None):
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, dict):
        if limit >= 1:
            data = {}
            for (k, v) in obj.items():
                data[k] = todict(v, limit - 1, classkey)
            return data
        else:
            return "class:" + obj.__class__.__name__
    elif isinstance(obj, Iterable):
        return [todict(val) for val in obj]
    elif hasattr(obj, "_ast"):
        return (
            {"ast": todict(obj._ast(), limit - 1)}
            if limit >= 1
            else {"class:" + obj.__class__.__name__}
        )
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return (
            {"__iter__": [todict(v, limit - 1, classkey) for v in obj]}
            if limit >= 1
            else {"class:" + obj.__class__.__name__}
        )
    elif hasattr(obj, "__dict__"):
        if limit >= 1:
            data = dict(
                [
                    (key, todict(value, limit - 1, classkey))
                    for key, value in obj.__dict__.items()
                    if not callable(value) and not key.startswith("_")
                ]
            )
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return "class:" + obj.__class__.__name__
    else:
        return obj


def format_fact(fact, fact_type):
    """Formats a fact into a desired format"""

    if fact_type in FactFormats.keys():
        if isinstance(fact, Iterable):
            reply = []
            for fact_entry in fact:
                part_reply = {}
                for fact_detail in FactFormats.get(fact_type):
                    part_reply.update(
                        {fact_detail: str(getattr(fact_entry, fact_detail))}
                    )
                reply.append(part_reply)
        else:
            reply = {}
            for fact_detail in FactFormats.get(fact_type):
                reply.update({fact_detail: str(getattr(fact, fact_detail))})
        return reply
    else:
        return todict(fact)
