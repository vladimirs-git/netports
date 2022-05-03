"""VLAN IDs"""

from typing import Any

from netports.ports import inumbers, ranges
from netports.ranges import Ranges
from netports.static import RANGE_SPLITTER_HPE, SPLITTER_HPE
from netports.types_ import LInt


# noinspection PyIncorrectDocstring
def ivlan(items: Any, **kwargs) -> LInt:
    """**Integer VLAN IDs** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :return: *List[int]* of unique sorted VLANs.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: "1,3-5"
        return: [1, 3, 4, 5]
    """
    vlans: LInt = inumbers(items, **kwargs)
    _check_vlan_ids(vlans)
    return vlans


def ivlan_all() -> LInt:
    """**All Integer VLAN IDs** - Full range of VLAN IDs.
    :return: *List[int]* All VLAN IDs.
    """
    return list(range(1, 4095))


def ivlan_hpe(items: Any) -> LInt:
    """**Integer VLAN IDs, for Hewlett Packard Enterprise** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :return: *List[int]* of unique sorted VLANs, for Hewlett Packard Enterprise.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: "1 3 to 5"
        return: [1, 3, 4, 5]
    """
    vlans: LInt = inumbers(items, splitter=SPLITTER_HPE, range_splitter=RANGE_SPLITTER_HPE)
    _check_vlan_ids(vlans)
    return vlans


# noinspection PyIncorrectDocstring
def svlan(items: Any, **kwargs) -> str:
    """**String VLAN IDs** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :return: *str* of unique sorted VLANs.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: [1, 3, 4, 5]
        return: "1,3-5"
    """
    ranges_: Ranges = ranges(items, **kwargs)
    _check_vlan_ids(ranges_.numbers)
    return str(ranges_)


def svlan_all() -> str:
    """**All String VLAN IDs** - Full range of VLAN IDs.
    :return: *str* All VLAN IDs.
    """
    return "1-4094"


def svlan_hpe(items: Any) -> str:
    """**String VLAN IDs, for Hewlett Packard Enterprise** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :return: *str* of unique sorted VLANs, for Hewlett Packard Enterprise.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: [1, 3, 4, 5]
        return: "1 3 to 5"
    """
    ranges_: Ranges = ranges(items, splitter=SPLITTER_HPE, range_splitter=RANGE_SPLITTER_HPE)
    _check_vlan_ids(ranges_.numbers)
    return str(ranges_)


# ============================= helpers ==============================

def _check_vlan_ids(items: LInt) -> bool:
    """True if all items are in the valid VLAN range 1...4094, else raise ValueError."""
    if invalid_vlan := [i for i in items if i < 1 or i > 4094]:
        raise ValueError(f"{invalid_vlan=}, expected in range 1...4094")
    return True
