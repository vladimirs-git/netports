"""VLAN IDs"""

from typing import Any

from netports.ports import inumbers, parse_range
from netports.range import Range
from netports.static import RANGE_SPLITTER, RANGE_SPLITTER_HPE, SPLITTER, SPLITTER_HPE
from netports.types_ import LInt


# noinspection PyIncorrectDocstring
def ivlan(items: Any = "", **kwargs) -> LInt:
    """**Integer VLAN IDs** - Sorting VLANs and removing duplicates
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates
    :param all: True - Return All VLAN IDs: [1, 2, ..., 4094]
    :param splitter: Separator character between items, by default ","
    :param range_splitter: Separator between min and max numbers in range, by default "-"
    :param platform: Set `splitter` and `range_splitter` to platform specific values.
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :return: *List[int]* of unique sorted VLANs
    :raises ValueError: if VLANs are outside valid range 1...4094

    :example:
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
    """**String VLAN IDs** - Sorting VLANs and removing duplicates
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates
    :param all: True - Return All VLAN IDs: "1-4094"
    :param splitter: Separator character between items, by default ","
    :param range_splitter: Separator between min and max numbers in range, by default "-"
    :param platform: Set `splitter` and `range_splitter` to platform specific values.
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :return: *str* of unique sorted VLANs
    :raises ValueError: if VLANs are outside valid range 1...4094

    :example:
        items: [1, 3, 4, 5]
        return: "1,3-5"
    """
    if bool(kwargs.get("all")):
        return "1-4094"
    kwargs = _update_splitters(**kwargs)
    range_o: Range = parse_range(items, **kwargs)
    _check_vlan_ids(range_o.numbers)
    return str(range_o)


# ============================= helpers ==============================

def _check_vlan_ids(items: LInt) -> bool:
    """Checks VLAN IDs
    :param items: VLAN IDs
    :return: True if all items are in the valid VLAN range 1...4094
    :raises ValueError: If on of item is outside valid range
    """
    if invalid_vlan := [i for i in items if i < 1 or i > 4094]:
        raise ValueError(f"{invalid_vlan=}, expected in range 1...4094")
    return True


def _update_splitters(**kwargs):
    """Updates `splitter` and `range_splitter` by `platform`.
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
