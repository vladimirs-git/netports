"""IP Protocols"""

from typing import Any, Tuple

from netports import helpers as h
from netports.ports import inumbers, snumbers
from netports.ranges import Ranges
from netports.types_ import LInt, LStr, DAny, DiAny

IP_PORTS: DiAny = {
    0: {"number": 0,
        "name": "hopopt",
        "description": "IPv6 Hop-by-Hop Option, RFC 8200"},
    1: {"number": 1,
        "name": "icmp",
        "description": "Internet Control Message Protocol, RFC 792"},
    2: {"number": 2,
        "name": "igmp",
        "description": "Internet Group Management Protocol, RFC 1112"},
    3: {"number": 3,
        "name": "ggp",
        "description": "Gateway-to-Gateway Protocol, RFC 823"},
    4: {"number": 4,
        "name": "ip-in-ip",
        "description": "IP in IP (encapsulation), RFC 2003"},
    5: {"number": 5,
        "name": "st",
        "description": "Internet Stream Protocol, RFC 1190, RFC 1819"},
    6: {"number": 6,
        "name": "tcp",
        "description": "Transmission Control Protocol, RFC 793"},
    7: {"number": 7,
        "name": "cbt",
        "description": "Core-based trees, RFC 2189"},
    8: {"number": 8,
        "name": "egp",
        "description": "Exterior Gateway Protocol, RFC 888"},
    9: {"number": 9,
        "name": "igp",
        "description": "Interior Gateway Protocol (Cisco IGRP)"},
    10: {"number": 10,
         "name": "bbn-rcc-mon",
         "description": "BBN RCC Monitoring"},
    11: {"number": 11,
         "name": "nvp-ii",
         "description": "Network Voice Protocol, RFC 741"},
    12: {"number": 12,
         "name": "pup",
         "description": "Xerox PUP"},
    13: {"number": 13,
         "name": "argus",
         "description": "ARGUS"},
    14: {"number": 14,
         "name": "emcon",
         "description": "EMCON"},
    15: {"number": 15,
         "name": "xnet",
         "description": "Cross Net Debugger, IEN 158"},
    16: {"number": 16,
         "name": "chaos",
         "description": "Chaos"},
    17: {"number": 17,
         "name": "udp",
         "description": "User Datagram Protocol, RFC 768"},
    18: {"number": 18,
         "name": "mux",
         "description": "Multiplexing, IEN 90"},
    19: {"number": 19,
         "name": "dcn-meas",
         "description": "DCN Measurement Subsystems"},
    20: {"number": 20,
         "name": "hmp",
         "description": "Host Monitoring Protocol, RFC 869"},
    21: {"number": 21,
         "name": "prm",
         "description": "Packet Radio Measurement"},
    22: {"number": 22,
         "name": "xns-idp",
         "description": "XEROX NS IDP"},
    23: {"number": 23,
         "name": "trunk-1",
         "description": "Trunk-1"},
    24: {"number": 24,
         "name": "trunk-2",
         "description": "Trunk-2"},
    25: {"number": 25,
         "name": "leaf-1",
         "description": "Leaf-1"},
    26: {"number": 26,
         "name": "leaf-2",
         "description": "Leaf-2"},
    27: {"number": 27,
         "name": "rdp",
         "description": "Reliable Data Protocol, RFC 908"},
    28: {"number": 28,
         "name": "irtp",
         "description": "Internet Reliable Transaction Protocol, RFC 938"},
    29: {"number": 29,
         "name": "iso-tp4",
         "description": "ISO Transport Protocol Class 4, RFC 905"},
    30: {"number": 30,
         "name": "netblt",
         "description": "Bulk Data Transfer Protocol, RFC 998"},
    31: {"number": 31,
         "name": "mfe-nsp",
         "description": "MFE Network Services Protocol"},
    32: {"number": 32,
         "name": "merit-inp",
         "description": "MERIT Internodal Protocol"},
    33: {"number": 33,
         "name": "dccp",
         "description": "Datagram Congestion Control Protocol, RFC 4340"},
    34: {"number": 34,
         "name": "3pc",
         "description": "Third Party Connect Protocol"},
    35: {"number": 35,
         "name": "idpr",
         "description": "Inter-Domain Policy Routing Protocol, RFC 1479"},
    36: {"number": 36,
         "name": "xtp",
         "description": "Xpress Transport Protocol"},
    37: {"number": 37,
         "name": "ddp",
         "description": "Datagram Delivery Protocol"},
    38: {"number": 38,
         "name": "idpr-cmtp",
         "description": "IDPR Control Message Transport Protocol"},
    39: {"number": 39,
         "name": "tp++",
         "description": "TP++ Transport Protocol"},
    40: {"number": 40,
         "name": "il",
         "description": "IL Transport Protocol"},
    41: {"number": 41,
         "name": "ipv6",
         "description": "IPv6 Encapsulation (6to4 and 6in4), RFC 2473"},
    42: {"number": 42,
         "name": "sdrp",
         "description": "Source Demand Routing Protocol, RFC 1940"},
    43: {"number": 43,
         "name": "ipv6-route",
         "description": "Routing Header for IPv6, RFC 8200"},
    44: {"number": 44,
         "name": "ipv6-frag",
         "description": "Fragment Header for IPv6, RFC 8200"},
    45: {"number": 45,
         "name": "idrp",
         "description": "Inter-Domain Routing Protocol"},
    46: {"number": 46,
         "name": "rsvp",
         "description": "Resource Reservation Protocol, RFC 2205"},
    47: {"number": 47,
         "name": "gre",
         "description": "Generic Routing Encapsulation, RFC 2784, RFC 2890"},
    48: {"number": 48,
         "name": "dsr",
         "description": "Dynamic Source Routing Protocol, RFC 4728"},
    49: {"number": 49,
         "name": "bna",
         "description": "Burroughs Network Architecture"},
    50: {"number": 50,
         "name": "esp",
         "description": "Encapsulating Security Payload, RFC 4303"},
    51: {"number": 51,
         "name": "ah",
         "description": "Authentication Header, RFC 4302"},
    52: {"number": 52,
         "name": "i-nlsp",
         "description": "Integrated Net Layer Security Protocol, TUBA"},
    53: {"number": 53,
         "name": "swipe",
         "description": "SwIPe, RFC 5237"},
    54: {"number": 54,
         "name": "narp",
         "description": "NBMA Address Resolution Protocol, RFC 1735"},
    55: {"number": 55,
         "name": "mobile",
         "description": "IP Mobility (Min Encap), RFC 2004"},
    56: {"number": 56,
         "name": "tlsp",
         "description": "Transport Layer Security Protocol (using Kryptonet key management)"},
    57: {"number": 57,
         "name": "skip",
         "description": "Simple Key-Management for Internet Protocol, RFC 2356"},
    58: {"number": 58,
         "name": "ipv6-icmp",
         "description": "ICMP for IPv6, RFC 4443, RFC 4884"},
    59: {"number": 59,
         "name": "ipv6-nonxt",
         "description": "No Next Header for IPv6, RFC 8200"},
    60: {"number": 60,
         "name": "ipv6-opts",
         "description": "Destination Options for IPv6, RFC 8200"},
    61: {"number": 61,
         "name": "any",
         "description": "host internal protocol"},
    62: {"number": 62,
         "name": "cftp",
         "description": "CFTP"},
    63: {"number": 63,
         "name": "any",
         "description": "local network"},
    64: {"number": 64,
         "name": "sat-expak",
         "description": "SATNET and Backroom EXPAK"},
    65: {"number": 65,
         "name": "kryptolan",
         "description": "Kryptolan"},
    66: {"number": 66,
         "name": "rvd",
         "description": "MIT Remote Virtual Disk Protocol"},
    67: {"number": 67,
         "name": "ippc",
         "description": "Internet Pluribus Packet Core"},
    68: {"number": 68,
         "name": "any",
         "description": "distributed file system"},
    69: {"number": 69,
         "name": "sat-mon",
         "description": "SATNET Monitoring"},
    70: {"number": 70,
         "name": "visa",
         "description": "VISA Protocol"},
    71: {"number": 71,
         "name": "ipcu",
         "description": "Internet Packet Core Utility"},
    72: {"number": 72,
         "name": "cpnx",
         "description": "Computer Protocol Network Executive"},
    73: {"number": 73,
         "name": "cphb",
         "description": "Computer Protocol Heart Beat"},
    74: {"number": 74,
         "name": "wsn",
         "description": "Wang Span Network"},
    75: {"number": 75,
         "name": "pvp",
         "description": "Packet Video Protocol"},
    76: {"number": 76,
         "name": "br-sat-mon",
         "description": "Backroom SATNET Monitoring"},
    77: {"number": 77,
         "name": "sun-nd",
         "description": "SUN ND PROTOCOL-Temporary"},
    78: {"number": 78,
         "name": "wb-mon",
         "description": "WIDEBAND Monitoring"},
    79: {"number": 79,
         "name": "wb-expak",
         "description": "WIDEBAND EXPAK"},
    80: {"number": 80,
         "name": "iso-ip",
         "description": "International Organization for Standardization Internet Protocol"},
    81: {"number": 81,
         "name": "vmtp",
         "description": "Versatile Message Transaction Protocol, RFC 1045"},
    82: {"number": 82,
         "name": "secure-vmtp",
         "description": "Secure Versatile Message Transaction Protocol, RFC 1045"},
    83: {"number": 83,
         "name": "vines",
         "description": "VINES"},
    84: {"number": 84,
         "name": "ttp",
         "description": "TTP"},
    # 84: {"number": 84,
    #      "name": "iptm",
    #      "description": "Internet Protocol Traffic Manager"},
    85: {"number": 85,
         "name": "nsfnet-igp",
         "description": "NSFNET-IGP"},
    86: {"number": 86,
         "name": "dgp",
         "description": "Dissimilar Gateway Protocol"},
    87: {"number": 87,
         "name": "tcf",
         "description": "TCF"},
    88: {"number": 88,
         "name": "eigrp",
         "description": "EIGRP, Informational RFC 7868"},
    89: {"number": 89,
         "name": "ospf",
         "description": "Open Shortest Path First, RFC 2328"},
    90: {"number": 90,
         "name": "sprite-rpc",
         "description": "Sprite RPC Protocol"},
    91: {"number": 91,
         "name": "larp",
         "description": "Locus Address Resolution Protocol"},
    92: {"number": 92,
         "name": "mtp",
         "description": "Multicast Transport Protocol"},
    93: {"number": 93,
         "name": "ax.25",
         "description": "AX.25"},
    94: {"number": 94,
         "name": "os",
         "description": "KA9Q NOS compatible IP over IP tunneling"},
    95: {"number": 95,
         "name": "micp",
         "description": "Mobile Internetworking Control Protocol"},
    96: {"number": 96,
         "name": "scc-sp",
         "description": "Semaphore Communications Sec. Pro"},
    97: {"number": 97,
         "name": "etherip",
         "description": "Ethernet-within-IP Encapsulation, RFC 3378"},
    98: {"number": 98,
         "name": "encap",
         "description": "Encapsulation Header, RFC 1241"},
    99: {"number": 99,
         "name": "any",
         "description": "private encryption scheme"},
    100: {"number": 100,
          "name": "gmtp",
          "description": "GMTP"},
    101: {"number": 101,
          "name": "ifmp",
          "description": "Ipsilon Flow Management Protocol"},
    102: {"number": 102,
          "name": "pnni",
          "description": "PNNI over IP"},
    103: {"number": 103,
          "name": "pim",
          "description": "Protocol Independent Multicast"},
    104: {"number": 104,
          "name": "aris",
          "description": "IBM ARIS (Aggregate Route IP Switching) Protocol"},
    105: {"number": 105,
          "name": "scps",
          "description": "SCPS (Space Communications Protocol Standards), SCPS-TP"},
    106: {"number": 106,
          "name": "qnx",
          "description": "QNX"},
    107: {"number": 107,
          "name": "a/n",
          "description": "Active Networks"},
    108: {"number": 108,
          "name": "ipcomp",
          "description": "IP Payload Compression Protocol, RFC 3173"},
    109: {"number": 109,
          "name": "snp",
          "description": "Sitara Networks Protocol"},
    110: {"number": 110,
          "name": "compaq-peer",
          "description": "Compaq Peer Protocol"},
    111: {"number": 111,
          "name": "ipx-in-ip",
          "description": "IPX in IP"},
    112: {"number": 112,
          "name": "vrrp",
          "description": "Virtual Router Redundancy Protocol, "
                         "Common Address Redundancy Protocol (not IANA assigned), 3768"},
    113: {"number": 113,
          "name": "pgm",
          "description": "PGM Reliable Transport Protocol, RFC 3208"},
    114: {"number": 114,
          "name": "any",
          "description": "0-hop protocol"},
    115: {"number": 115,
          "name": "l2tp",
          "description": "Layer Two Tunneling Protocol Version 3, RFC 3931"},
    116: {"number": 116,
          "name": "ddx",
          "description": "D-II Data Exchange (DDX)"},
    117: {"number": 117,
          "name": "iatp",
          "description": "Interactive Agent Transfer Protocol"},
    118: {"number": 118,
          "name": "stp",
          "description": "Schedule Transfer Protocol"},
    119: {"number": 119,
          "name": "srp",
          "description": "SpectraLink Radio Protocol"},
    120: {"number": 120,
          "name": "uti",
          "description": "Universal Transport Interface Protocol"},
    121: {"number": 121,
          "name": "smp",
          "description": "Simple Message Protocol"},
    122: {"number": 122,
          "name": "sm",
          "description": "Simple Multicast Protocol, draft-perlman-simple-multicast-03"},
    123: {"number": 123,
          "name": "ptp",
          "description": "Performance Transparency Protocol"},
    124: {"number": 124,
          "name": "is-is",
          "description": "Intermediate System to Intermediate System (IS-IS) Protocol over IPv4, "
                         "RFC 1142 and RFC 1195"},
    125: {"number": 125,
          "name": "fire",
          "description": "Flexible Intra-AS Routing Environment"},
    126: {"number": 126,
          "name": "crtp",
          "description": "Combat Radio Transport Protocol"},
    127: {"number": 127,
          "name": "crudp",
          "description": "Combat Radio User Datagram"},
    128: {"number": 128,
          "name": "sscopmce",
          "description": "Service-Specific Connection-Oriented Protocol in a Multilink and "
                         "Connectionless Environment, ITU-T Q.2111 (1999)"},
    129: {"number": 129,
          "name": "iplt",
          "description": ""},
    130: {"number": 130,
          "name": "sps",
          "description": "Secure Packet Shield"},
    131: {"number": 131,
          "name": "pipe",
          "description": "Private IP Encapsulation within IP, "
                         "Expired I-D draft-petri-mobileip-pipe-00.txt"},
    132: {"number": 132,
          "name": "sctp",
          "description": "Stream Control Transmission Protocol, "
                         "RFC 4960"},
    133: {"number": 133,
          "name": "fc",
          "description": "Fibre Channel"},
    134: {"number": 134,
          "name": "rsvp-e2e-ignore",
          "description": "Reservation Protocol (RSVP) End-to-End Ignore, RFC 3175"},
    135: {"number": 135,
          "name": "mobility",
          "description": "Header, Mobility Extension Header for IPv6, RFC 6275"},
    136: {"number": 136,
          "name": "udplite",
          "description": "Lightweight User Datagram Protocol, RFC 3828"},
    137: {"number": 137,
          "name": "mpls-in-ip",
          "description": "Multiprotocol Label Switching Encapsulated in IP, RFC 4023, RFC 5332"},
    138: {"number": 138,
          "name": "manet",
          "description": "MANET Protocols, RFC 5498"},
    139: {"number": 139,
          "name": "hip",
          "description": "Host Identity Protocol, RFC 5201"},
    140: {"number": 140,
          "name": "shim6",
          "description": "Site Multihoming by IPv6 Intermediation, RFC 5533"},
    141: {"number": 141,
          "name": "wesp",
          "description": "Wrapped Encapsulating Security Payload, RFC 5840"},
    142: {"number": 142,
          "name": "rohc",
          "description": "Robust Header Compression, RFC 5856"},
    143: {"number": 143,
          "name": "ethernet",
          "description": "IPv6 Segment Routing "
                         "(TEMPORARY - registered 2020-01-31, expired 2021-01-31)"},

}

IP_NAMES: DAny = {d["name"]: d for i, d in IP_PORTS.items()}


# noinspection PyIncorrectDocstring
def iip(items: Any = "", **kwargs) -> LInt:
    """**Integer IP protocol numbers** - Sort numbers and remove duplicates.
    :param items: Range of IP protocol numbers or *List[int]*, can be unsorted and with duplicates.
        "ip" - Return all IP protocol numbers: [0, 1, ..., 255]
    :param all: True - Return all IP protocol numbers: [0, 1, ..., 255]
    :return: *List[int]* of unique sorted IP protocol numbers.
        Raise *ValueError* if IP protocol numbers are outside valid range 0...255.
    Example1:
        items: "icmp,tcp,7,255"
        return: [1, 6, 7, 255]
    Example2:
        items: "ip"
        return: [0, 1, ... 254, 255]
    """
    if bool(kwargs.get("all")):
        return list(range(0, 256))
    items_ = [s.lower() for s in h.split(items)]
    numbers, names = iip_nip(items_)
    if "ip" in names:
        return list(range(0, 256))
    numbers_ = [IP_NAMES[s]["number"] for s in names]
    numbers.extend(numbers_)
    return inumbers(numbers)


def iip_nip(items: Any) -> Tuple[LInt, LStr]:
    """**IP protocol Numbers and Names** - Split numbers and names and remove duplicates.
    :param items: Range of IP protocol numbers and names, can be unsorted and with duplicates.
    :return: List of IP protocol Numbers and List of IP protocol Names.
        Raise *ValueError* if IP protocol number are outside valid range 0...255.
        Raise *ValueError* if IP protocol name is unknown.
    Example:
        items: ["icmp", "tcp", "7", 255]
        return: [7, 255] ["icmp", "tcp"]
    """
    items_ = [s.lower() for s in h.split(items)]
    if "ip" in items_:
        return list(range(0, 256)), ["ip"]

    numbers: LInt = []
    names: LStr = []
    for item_ in items_:
        try:
            ranges_o = Ranges(item_)
            numbers.extend(ranges_o.numbers)
        except ValueError:
            names.append(item_)
    numbers = sorted(set(numbers))
    _check_ip_numbers(numbers)
    names = sorted(set(names))
    _check_ip_names(names)
    return numbers, names


# noinspection PyIncorrectDocstring
def sip(items: Any = "", **kwargs) -> str:
    """**String IP protocol numbers** - Sort numbers and remove duplicates.
    :param items: Range of IP protocol numbers or *List[int]*, can be unsorted and with duplicates.
        "ip" - mean all numbers in range 0...255.
    :param all: True - Return all IP protocol numbers: "0-255"
    :return: *str* of unique sorted IP protocol numbers.
        Raise *ValueError* if IP protocol numbers are outside valid range 0...255.
    Example:
        items: ["icmp", "tcp", "7", 255]
        return: "1,6-7,255"
    """
    if bool(kwargs.get("all")):
        return "0-255"
    numbers = iip(items)
    return snumbers(numbers)


# ============================= helpers ==============================

def _check_ip_numbers(items: LInt) -> bool:
    """True if all items are in the valid IP range 0...255, else raise ValueError."""
    if invalid_ip_numbers := [i for i in items if i < 0 or i > 255]:
        raise ValueError(f"{invalid_ip_numbers=}, expected in range 0...255")
    return True


def _check_ip_names(items: LStr) -> bool:
    """True if all items are in the valid IANA range, else raise ValueError."""
    if invalid_ip_names := [s for s in items if s not in IP_NAMES]:
        raise ValueError(f"{invalid_ip_names=}")
    return True
