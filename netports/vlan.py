"""VLAN IDs"""

from typing import Any

from netports.ports import inumbers, ranges
from netports.ranges import Ranges
from netports.static import RANGE_SPLITTER, RANGE_SPLITTER_HPE, SPLITTER, SPLITTER_HPE
from netports.types_ import LInt


# noinspection PyIncorrectDocstring
def ivlan(items: Any = "", **kwargs) -> LInt:
    """**Integer VLAN IDs** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :param all: True - Return All VLAN IDs: [1, 2, ..., 4094].
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :param platform: Set `splitter` and `range_splitter` to platform specific values
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :return: *List[int]* of unique sorted VLANs.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: "1,3-5"
        return: [1, 3, 4, 5]
    """
    if bool(kwargs.get("all")):
        return list(range(1, 4095))
    kwargs = _update_splitters(**kwargs)
    vlans: LInt = inumbers(items, **kwargs)
    _check_vlan_ids(vlans)
    return vlans


# noinspection PyIncorrectDocstring
def svlan(items: Any = "", **kwargs) -> str:
    """**String VLAN IDs** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :param all: True - Return All VLAN IDs: "1-4094".
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :param platform: Set `splitter` and `range_splitter` to platform specific values
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :return: *str* of unique sorted VLANs.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: [1, 3, 4, 5]
        return: "1,3-5"
    """
    if bool(kwargs.get("all")):
        return "1-4094"
    kwargs = _update_splitters(**kwargs)
    ranges_: Ranges = ranges(items, **kwargs)
    _check_vlan_ids(ranges_.numbers)
    return str(ranges_)


# ============================= helpers ==============================

def _check_vlan_ids(items: LInt) -> bool:
    """True if all items are in the valid VLAN range 1...4094, else raise ValueError."""
    if invalid_vlan := [i for i in items if i < 1 or i > 4094]:
        raise ValueError(f"{invalid_vlan=}, expected in range 1...4094")
    return True


def _update_splitters(**kwargs):
    """Update `splitter` and `range_splitter` by `platform`.
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    """
    platform = str(kwargs.get("platform") or "")
    if platform == "cisco":
        return {**kwargs, **{"splitter": SPLITTER, "range_splitter": RANGE_SPLITTER}}
    if platform == "hpe":
        return {**kwargs, **{"splitter": SPLITTER_HPE, "range_splitter": RANGE_SPLITTER_HPE}}
    return kwargs
