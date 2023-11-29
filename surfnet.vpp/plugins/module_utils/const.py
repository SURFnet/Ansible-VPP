# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

VPP_DEFAULT_DIR = "/usr/share/vpp/api"
VPP_SOCKET_DIR = "/var/sockets"

FactFormats = {
    # sw_bond_interface_details(_0=841, context=4, sw_if_index=3, id=0, mode=<vl_api_bond_mode_t.BOND_API_MODE_LACP: 5>,
    # lb=<vl_api_bond_lb_algo_t.BOND_API_LB_ALGO_L2: 0>, numa_only=False, active_members=2, members=2,
    # interface_name='BondEthernet0')
    "sw_bond_interface_dump": [
        "interface_name",
        "sw_if_index",
        "mode",
        "lb",
        "numa_only",
        "active_members",
        "members",
    ],
    # bridge_domain_details(_0=794, context=3, bd_id=2813, flood=True, uu_flood=True, forward=False, learn=True,
    # arp_term=False, arp_ufwd=False, mac_age=0, bd_tag='2813', bvi_sw_if_index=4294967295,
    # uu_fwd_sw_if_index=4294967295, n_sw_ifs=2, sw_if_details=[vl_api_bridge_domain_sw_if_t(context=0, sw_if_index=96,
    # shg=0), vl_api_bridge_domain_sw_if_t(context=0, sw_if_index=95, shg=0)])
    "bridge_domain_dump": [
        "bd_id",
        "flood",
        "uu_flood",
        "forward",
        "learn",
        "arp_term",
        "arp_ufwd",
        "mac_age",
        "bd_tag",
    ],
    # sw_interface_details(_0=674, context=2, sw_if_index=7, sup_sw_if_index=7,
    # l2_address=MACAddress(02:fe:29:40:69:83), flags=<vl_api_if_status_flags_t.IF_STATUS_API_FLAG_ADMIN_UP: 1>,
    # type=<vl_api_if_type_t.IF_API_TYPE_HARDWARE: 0>, link_duplex=<vl_api_link_duplex_t.LINK_DUPLEX_API_UNKNOWN: 0>,
    # link_speed=0, link_mtu=9000, mtu=[9000, 0, 0, 0], sub_id=0, sub_number_of_tags=0, sub_outer_vlan_id=0,
    # sub_inner_vlan_id=0, sub_if_flags=<vl_api_sub_if_flags_t.0: 0>, vtr_op=0, vtr_push_dot1q=0, vtr_tag1=0,
    # vtr_tag2=0, outer_tag=0, b_dmac=MACAddress(00:00:00:00:00:00), b_smac=MACAddress(00:00:00:00:00:00), b_vlanid=0,
    # i_sid=0, interface_name='VirtualEthernet0/0/27', interface_dev_type='vhost-user', tag='ttien_tien-4004')
    "sw_interface_dump": [
        "interface_name",
        "sw_if_index",
        "sup_sw_if_index",
        "flags",
        "type",
        "link_mtu",
        "interface_dev_type",
        "tag",
    ],
}


class L2_VTR_OP:
    L2_DISABLED = 0
    L2_PUSH_1 = 1
    L2_PUSH_2 = 2
    L2_POP_1 = 3
    L2_POP_2 = 4
    L2_TRANSLATE_1_1 = 5
    L2_TRANSLATE_1_2 = 6
    L2_TRANSLATE_2_1 = 7
    L2_TRANSLATE_2_2 = 8


class BRIDGE_API_FLAGS:
    BRIDGE_API_FLAG_NONE = 0
    BRIDGE_API_FLAG_LEARN = 1
    BRIDGE_API_FLAG_FWD = 2
    BRIDGE_API_FLAG_FLOOD = 4
    BRIDGE_API_FLAG_UU_FLOOD = 8
    BRIDGE_API_FLAG_ARP_TERM = 16
    BRIDGE_API_FLAG_ARP_UFWD = 32


class VPPModuleMethods:
    GET = "get"
    SET = "set"
    DELETE = "delete"
    PRESENT = "present"
    ABSENT = "absent"


# Borrowed from https://github.com/FDio/vpp/blob/master/src/vnet/api_errno.h
class VPPErrors:
    ERRORS = [
        ("UNSPECIFIED", -1, "Unspecified Error"),
        ("INVALID_SW_IF_INDEX", -2, "Invalid sw_if_index"),
        ("NO_SUCH_FIB", -3, "No such FIB / VRF"),
        ("NO_SUCH_INNER_FIB", -4, "No such inner FIB / VRF"),
        ("NO_SUCH_LABEL", -5, "No such label"),
        ("NO_SUCH_ENTRY", -6, "No such entry"),
        ("INVALID_VALUE", -7, "Invalid value"),
        ("INVALID_VALUE_2", -8, "Invalid value #2"),
        ("UNIMPLEMENTED", -9, "Unimplemented"),
        ("INVALID_SW_IF_INDEX_2", -10, "Invalid sw_if_index #2"),
        ("SYSCALL_ERROR_1", -11, "System call error #1"),
        ("SYSCALL_ERROR_2", -12, "System call error #2"),
        ("SYSCALL_ERROR_3", -13, "System call error #3"),
        ("SYSCALL_ERROR_4", -14, "System call error #4"),
        ("SYSCALL_ERROR_5", -15, "System call error #5"),
        ("SYSCALL_ERROR_6", -16, "System call error #6"),
        ("SYSCALL_ERROR_7", -17, "System call error #7"),
        ("SYSCALL_ERROR_8", -18, "System call error #8"),
        ("SYSCALL_ERROR_9", -19, "System call error #9"),
        ("SYSCALL_ERROR_10", -20, "System call error #10"),
        ("FEATURE_DISABLED", -30, "Feature disabled by configuration"),
        ("INVALID_REGISTRATION", -31, "Invalid registration"),
        ("NEXT_HOP_NOT_IN_FIB", -50, "Next hop not in FIB"),
        ("UNKNOWN_DESTINATION", -51, "Unknown destination"),
        ("NO_PATHS_IN_ROUTE", -52, "No paths specified in route"),
        ("NEXT_HOP_NOT_FOUND_MP", -53, "Next hop not found multipath"),
        ("NO_MATCHING_INTERFACE", -54, "No matching interface for probe"),
        ("INVALID_VLAN", -55, "Invalid VLAN"),
        ("VLAN_ALREADY_EXISTS", -56, "VLAN subif already exists"),
        ("INVALID_SRC_ADDRESS", -57, "Invalid src address"),
        ("INVALID_DST_ADDRESS", -58, "Invalid dst address"),
        ("ADDRESS_LENGTH_MISMATCH", -59, "Address length mismatch"),
        ("ADDRESS_NOT_FOUND_FOR_INTERFACE", -60, "Address not found for interface"),
        ("ADDRESS_NOT_DELETABLE", -61, "Address not deletable"),
        ("IP6_NOT_ENABLED", -62, "ip6 not enabled"),
        ("NO_SUCH_NODE", -63, "No such graph node"),
        ("NO_SUCH_NODE2", -64, "No such graph node #2"),
        ("NO_SUCH_TABLE", -65, "No such table"),
        ("NO_SUCH_TABLE2", -66, "No such table #2"),
        ("NO_SUCH_TABLE3", -67, "No such table #3"),
        ("SUBIF_ALREADY_EXISTS", -68, "Subinterface already exists"),
        ("SUBIF_CREATE_FAILED", -69, "Subinterface creation failed"),
        ("INVALID_MEMORY_SIZE", -70, "Invalid memory size requested"),
        ("INVALID_INTERFACE", -71, "Invalid interface"),
        (
            "INVALID_VLAN_TAG_COUNT",
            -72,
            "Invalid number of tags for requested operation",
        ),
        ("INVALID_ARGUMENT", -73, "Invalid argument"),
        ("UNEXPECTED_INTF_STATE", -74, "Unexpected interface state"),
        ("TUNNEL_EXIST", -75, "Tunnel already exists"),
        ("INVALID_DECAP_NEXT", -76, "Invalid decap-next"),
        ("RESPONSE_NOT_READY", -77, "Response not ready"),
        ("NOT_CONNECTED", -78, "Not connected to the data plane"),
        ("IF_ALREADY_EXISTS", -79, "Interface already exists"),
        (
            "BOND_SLAVE_NOT_ALLOWED",
            -80,
            "Operation not allowed on slave of BondEthernet",
        ),
        ("VALUE_EXIST", -81, "Value already exists"),
        ("SAME_SRC_DST", -82, "Source and destination are the same"),
        ("IP6_MULTICAST_ADDRESS_NOT_PRESENT", -83, "IP6 multicast address required"),
        ("SR_POLICY_NAME_NOT_PRESENT", -84, "Segment routing policy name required"),
        ("NOT_RUNNING_AS_ROOT", -85, "Not running as root"),
        ("ALREADY_CONNECTED", -86, "Connection to the data plane already exists"),
        ("UNSUPPORTED_JNI_VERSION", -87, "Unsupported JNI version"),
        ("IP_PREFIX_INVALID", -88, "IP prefix invalid (masked bits set in address)"),
        ("INVALID_WORKER", -89, "Invalid worker thread"),
        ("LISP_DISABLED", -90, "LISP is disabled"),
        ("CLASSIFY_TABLE_NOT_FOUND", -91, "Classify table not found"),
        ("INVALID_EID_TYPE", -92, "Unsupported LISP EID type"),
        ("CANNOT_CREATE_PCAP_FILE", -93, "Cannot create pcap file"),
        ("INCORRECT_ADJACENCY_TYPE", -94, "Invalid adjacency type for this operation"),
        (
            "EXCEEDED_NUMBER_OF_RANGES_CAPACITY",
            -95,
            "Operation would exceed configured capacity of ranges",
        ),
        (
            "EXCEEDED_NUMBER_OF_PORTS_CAPACITY",
            -96,
            "Operation would exceed capacity of number of ports",
        ),
        ("INVALID_ADDRESS_FAMILY", -97, "Invalid address family"),
        ("INVALID_SUB_SW_IF_INDEX", -98, "Invalid sub-interface sw_if_index"),
        ("TABLE_TOO_BIG", -99, "Table too big"),
        ("CANNOT_ENABLE_DISABLE_FEATURE", -100, "Cannot enable/disable feature"),
        ("BFD_EEXIST", -101, "Duplicate BFD object"),
        ("BFD_ENOENT", -102, "No such BFD object"),
        ("BFD_EINUSE", -103, "BFD object in use"),
        ("BFD_NOTSUPP", -104, "BFD feature not supported"),
        ("ADDRESS_IN_USE", -105, "Address in use"),
        ("ADDRESS_NOT_IN_USE", -106, "Address not in use"),
        ("QUEUE_FULL", -107, "Queue full"),
        ("APP_UNSUPPORTED_CFG", -108, "Unsupported application config"),
        ("URI_FIFO_CREATE_FAILED", -109, "URI FIFO segment create failed"),
        ("LISP_RLOC_LOCAL", -110, "RLOC address is local"),
        ("BFD_EAGAIN", -111, "BFD object cannot be manipulated at this time"),
        ("INVALID_GPE_MODE", -112, "Invalid GPE mode"),
        ("LISP_GPE_ENTRIES_PRESENT", -113, "LISP GPE entries are present"),
        ("ADDRESS_FOUND_FOR_INTERFACE", -114, "Address found for interface"),
        ("SESSION_CONNECT", -115, "Session failed to connect"),
        ("ENTRY_ALREADY_EXISTS", -116, "Entry already exists"),
        ("SVM_SEGMENT_CREATE_FAIL", -117, "Svm segment create fail"),
        ("APPLICATION_NOT_ATTACHED", -118, "Application not attached"),
        ("BD_ALREADY_EXISTS", -119, "Bridge domain already exists"),
        ("BD_IN_USE", -120, "Bridge domain has member interfaces"),
        ("BD_NOT_MODIFIABLE", -121, "Bridge domain 0 can't be deleted/modified"),
        ("BD_ID_EXCEED_MAX", -122, "Bridge domain ID exceeds 16M limit"),
        ("SUBIF_DOESNT_EXIST", -123, "Subinterface doesn't exist"),
        (
            "L2_MACS_EVENT_CLINET_PRESENT",
            -124,
            "Client already exist for L2 MACs events",
        ),
        ("INVALID_QUEUE", -125, "Invalid queue"),
        ("UNSUPPORTED", -126, "Unsupported"),
        ("DUPLICATE_IF_ADDRESS", -127, "Address already present on another interface"),
        ("APP_INVALID_NS", -128, "Invalid application namespace"),
        ("APP_WRONG_NS_SECRET", -129, "Wrong app namespace secret"),
        ("APP_CONNECT_SCOPE", -130, "Connect scope"),
        ("APP_ALREADY_ATTACHED", -131, "App already attached"),
        ("SESSION_REDIRECT", -132, "Redirect failed"),
        ("ILLEGAL_NAME", -133, "Illegal name"),
        ("NO_NAME_SERVERS", -134, "No name servers configured"),
        ("NAME_SERVER_NOT_FOUND", -135, "Name server not found"),
        ("NAME_RESOLUTION_NOT_ENABLED", -136, "Name resolution not enabled"),
        ("NAME_SERVER_FORMAT_ERROR", -137, "Server format error (bug!)"),
        ("NAME_SERVER_NO_SUCH_NAME", -138, "No such name"),
        ("NAME_SERVER_NO_ADDRESSES", -139, "No addresses available"),
        ("NAME_SERVER_NEXT_SERVER", -140, "Retry with new server"),
        ("APP_CONNECT_FILTERED", -141, "Connect was filtered"),
        ("ACL_IN_USE_INBOUND", -142, "Inbound ACL in use"),
        ("ACL_IN_USE_OUTBOUND", -143, "Outbound ACL in use"),
        ("INIT_FAILED", -144, "Initialization Failed"),
        ("NETLINK_ERROR", -145, "Netlink error"),
        ("BIER_BSL_UNSUP", -146, "BIER bit-string-length unsupported"),
        ("INSTANCE_IN_USE", -147, "Instance in use"),
        ("INVALID_SESSION_ID", -148, "Session ID out of range"),
        ("ACL_IN_USE_BY_LOOKUP_CONTEXT", -149, "ACL in use by a lookup context"),
        ("INVALID_VALUE_3", -150, "Invalid value #3"),
        ("NON_ETHERNET", -151, "Interface is not an Ethernet interface"),
        ("BD_ALREADY_HAS_BVI", -152, "Bridge domain already has a BVI interface"),
        ("INVALID_PROTOCOL", -153, "Invalid Protocol"),
        ("INVALID_ALGORITHM", -154, "Invalid Algorithm"),
        ("RSRC_IN_USE", -155, "Resource In Use"),
        ("KEY_LENGTH", -156, "invalid Key Length"),
        ("FIB_PATH_UNSUPPORTED_NH_PROTO", -157, "Unsupported FIB Path protocol"),
        ("API_ENDIAN_FAILED", -159, "Endian mismatch detected"),
        ("NO_CHANGE", -160, "No change in table"),
        ("MISSING_CERT_KEY", -161, "Missing certifcate or key"),
        ("LIMIT_EXCEEDED", -162, "limit exceeded"),
        ("IKE_NO_PORT", -163, "port not managed by IKE"),
        ("UDP_PORT_TAKEN", -164, "UDP port already taken"),
        ("EAGAIN", -165, "Retry stream call with cursor"),
        ("INVALID_VALUE_4", -166, "Invalid value #4"),
    ]


class GatherDetails:
    ARP = ["proxy_arp_dump", "proxy_arp_intfc_dump"]
    BFD = ["bfd_udp_session_dump", "bfd_auth_keys_dump"]
    BIER = [
        "bier_table_dump",
        "bier_imp_dump",
        "bier_disp_table_dump",
        "bier_disp_entry_dump",
    ]
    BOND = [
        "sw_interface_bond_dump",
        "sw_bond_interface_dump",
        "sw_interface_slave_dump",
        "sw_member_interface_dump",
    ]
    CLASSIFY = ["policer_classify_dump", "classify_session_dump", "flow_classify_dump"]
    FIB = ["fib_source_dump"]
    INTERFACE = ["sw_interface_dump", "sw_interface_rx_placement_dump"]
    IP = [
        "ip_table_dump",
        "ip_route_dump",
        "ip_mtable_dump",
        "ip_mroute_dump",
        "ip_address_dump",
        "ip_unnumbered_dump",
        "ip_dump",
        "mfib_signal_dump",
        "ip_punt_redirect_dump",
        "ip_container_proxy_dump",
        "ip_route_v2_dump",
        "ip_punt_redirect_v2_dump",
    ]
    IP6_ND = ["sw_interface_ip6nd_ra_dump", "ip6nd_proxy_dump"]
    IP_NEIGHBOR = ["ip_neighbor_dump"]
    IPFIX_EXPORT = [
        "ipfix_exporter_dump",
        "ipfix_classify_stream_dump",
        "ipfix_classify_table_dump",
    ]
    IPIP = ["ipip_tunnel_dump"]
    IPSEC = [
        "ipsec_spds_dump",
        "ipsec_spd_dump",
        "ipsec_tunnel_protect_dump",
        "ipsec_spd_interface_dump",
        "ipsec_itf_dump",
        "ipsec_sa_dump",
        "ipsec_sa_v2_dump",
        "ipsec_sa_v3_dump",
    ]
    L2 = [
        "l2_xconnect_dump",
        "l2_fib_table_dump",
        "bridge_domain_dump",
        "bd_ip_mac_dump",
    ]
    MPLS = ["mpls_tunnel_dump", "mpls_table_dump", "mpls_route_dump"]
    PIPE = ["pipe_dump"]
    POLICER = ["policer_dump", "policer_dump_v2"]
    PUNT = ["punt_socket_dump", "punt_reason_dump"]
    QOS = ["qos_store_dump", "qos_record_dump", "qos_egress_map_dump", "qos_mark_dump"]
    SESSION = ["session_rules_dump"]
    SPAN = ["sw_interface_span_dump"]
    SR = [
        "sr_localsids_dump",
        "sr_localsids_with_packet_stats_dump",
        "sr_policies_dump",
        "sr_policies_with_sl_index_dump",
        "sr_steering_pol_dump",
        "sr_policies_v2_dump",
    ]
    SR_PT = ["sr_pt_iface_dump"]
    TAPV2 = ["sw_interface_tap_v2_dump"]
    TEIB = ["teib_dump"]
    UDP = ["udp_encap_dump"]
    VIRTIO = ["sw_interface_virtio_pci_dump"]
    VPE = ["log_dump"]
    VXLAN_GPE = ["vxlan_gpe_tunnel_dump", "vxlan_gpe_tunnel_v2_dump"]

    COMMON = ["sw_interface_dump", "bridge_domain_dump", "sw_bond_interface_dump"]
    # COMMON = ['bridge_domain_dump']
    CORE = (
        ARP
        + BFD
        + BIER
        + BOND
        + CLASSIFY
        + FIB
        + INTERFACE
        + IP
        + IP6_ND
        + IP_NEIGHBOR
        + IPFIX_EXPORT
        + IPIP
        + IPSEC
        + L2
        + MPLS
        + PIPE
        + POLICER
        + PUNT
        + QOS
        + SESSION
        + SPAN
        + SR
        + SR_PT
        + TAPV2
        + TEIB
        + UDP
        + VIRTIO
        + VPE
        + VXLAN_GPE
    )
    ALL = CORE
