"""netports"""

from netports.interface4 import Interface4
from netports.ports import iports, itcp, ivlan, ivlan_hpe, ranges, sports, stcp, svlan, svlan_hpe
from netports.range import Range
from netports.ranges import Ranges

__all__ = [
    "Interface4",
    "Range",
    "Ranges",
    "iports",
    "itcp",
    "ivlan",
    "ivlan_hpe",
    "ranges",
    "sports",
    "stcp",
    "svlan",
    "svlan_hpe",
]

__version__ = "0.1.1"
__date__ = "2022-05-02"
__title__ = "netports"

__summary__ = ""
__author__ = "Vladimir Prusakov"
__email__ = "vladimir.prusakovs@gmail.com"
__url__ = "https://github.com/vladimirs-git/netports"
__download_url__ = f"{__url__}/archive/refs/tags/{__version__}.tar.gz"
__license__ = "MIT"
