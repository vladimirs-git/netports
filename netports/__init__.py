"""netports"""

from netports.interface4 import Interface4
from netports.ip import IP_NAMES, IP_PORTS, iip, iip_all, iip_nip, sip, sip_all
from netports.ports import inumbers, ranges, snumbers
from netports.range import Range
from netports.ranges import Ranges
from netports.tcp import itcp_all, stcp_all, stcp, itcp
from netports.vlan import ivlan_all, svlan_all, ivlan, ivlan_hpe, svlan, svlan_hpe

__all__ = [
    "IP_NAMES",
    "IP_PORTS",
    "Interface4",
    "Range",
    "Ranges",
    "iip",
    "iip_all",
    "iip_nip",
    "inumbers",
    "itcp",
    "itcp_all",
    "ivlan",
    "ivlan_all",
    "ivlan_hpe",
    "ranges",
    "sip",
    "sip_all",
    "snumbers",
    "stcp",
    "stcp_all",
    "svlan",
    "svlan_all",
    "svlan_hpe",
]

__version__ = "0.2.0"
__date__ = "2022-05-03"
__title__ = "netports"

__summary__ = ""
__author__ = "Vladimir Prusakov"
__email__ = "vladimir.prusakovs@gmail.com"
__url__ = "https://github.com/vladimirs-git/netports"
__download_url__ = f"{__url__}/archive/refs/tags/{__version__}.tar.gz"
__license__ = "MIT"
