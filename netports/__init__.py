"""netports"""

from netports.interface4 import Interface4
from netports.ip import IP_NAMES, IP_NUMBERS, iip, sip, ip_pairs
from netports.item import Item
from netports.ports import inumbers, parse_range, snumbers
from netports.range import Range
from netports.tcp import stcp, itcp
from netports.vlan import ivlan, svlan

__all__ = [
    "IP_NAMES",
    "IP_NUMBERS",
    "Interface4",
    "Item",
    "Range",
    "iip",
    "inumbers",
    "ip_pairs",
    "itcp",
    "ivlan",
    "parse_range",
    "sip",
    "snumbers",
    "stcp",
    "svlan",
]

__version__ = "0.5.2"
__date__ = "2022-07-30"
__title__ = "netports"

__summary__ = "A collection of Python objects and functions for managing ranges of VLANs, " \
              "TCP/UDP ports, IP protocol numbers, interfaces."
__author__ = "Vladimir Prusakov"
__email__ = "vladimir.prusakovs@gmail.com"
__url__ = "https://github.com/vladimirs-git/netports"
__download_url__ = f"{__url__}/archive/refs/tags/{__version__}.tar.gz"
__license__ = "MIT"
