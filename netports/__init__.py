"""netports"""

from netports.interface4 import Interface4
from netports.ip import IP_NAMES, IP_PORTS, iip, nip, sip
from netports.ports import inumbers, ranges, snumbers
from netports.range import Range
from netports.ranges import Ranges
from netports.tcp import stcp, itcp
from netports.vlan import ivlan, svlan

__all__ = [
    "IP_NAMES",
    "IP_PORTS",
    "Interface4",
    "Range",
    "Ranges",
    "iip",
    "inumbers",
    "itcp",
    "ivlan",
    "nip",
    "ranges",
    "sip",
    "snumbers",
    "stcp",
    "svlan",
]

__version__ = "0.2.0"
__date__ = "2022-05-04"
__title__ = "netports"

__summary__ = ""
__author__ = "Vladimir Prusakov"
__email__ = "vladimir.prusakovs@gmail.com"
__url__ = "https://github.com/vladimirs-git/netports"
__download_url__ = f"{__url__}/archive/refs/tags/{__version__}.tar.gz"
__license__ = "MIT"
