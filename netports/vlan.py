"""VLAN IDs"""

from typing import Any

from netports import helpers as h
from netports.ports import inumbers, parse_range
from netports.range import Range
from netports.static import BRIEF_ALL_I, RANGE_SPLITTER, RANGE_SPLITTER_HPE, SPLITTER, SPLITTER_HPE
from netports.types_ import LInt

MIN_VLAN = 1
MAX_VLAN = 4094
ALL_VLANS_L = list(range(MIN_VLAN, MAX_VLAN + 1))
ALL_VLANS_S = f"{MIN_VLAN}-{MAX_VLAN}"


# noinspection PyIncorrectDocstring
def ivlan(items: Any = "", **kwargs) -> LInt:
    """**Integer VLAN IDs** - Sorting VLANs and removing duplicates
    :param items: Range of VLANs, can be unsorted and with duplicates,
        *str, List[int], List[str]*
    :param bool verbose: True - all VLAN IDs in verbose mode: [1, 2, ..., 65535],
                         False - all VLAN IDs in brief mode: [-1] (reduces RAM usage),
                         by default False
    :param bool all: True - Returns all VLAN IDs: [1, 2, ..., 4094], or [-1] for verbose=False
    :param splitter: Separator character between items, by default ","
    :param range_splitter: Separator between min and max numbers in range, by default "-"
    :param platform: Set `splitter` and `range_splitter` to platform specific values
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
    if h.is_all(**kwargs):
        if h.is_brief(**kwargs):
            return [BRIEF_ALL_I]
        return ALL_VLANS_L.copy()
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = h.remove_brief_items(items)
            ports = inumbers(items_)
            _check_vlans(ports)
            return [BRIEF_ALL_I]

    kwargs = _update_splitters(**kwargs)
    vlans: LInt = inumbers(items, **kwargs)
    _check_vlans(vlans)

    if h.is_brief(**kwargs):
        if vlans == ALL_VLANS_L:
            return [BRIEF_ALL_I]
    return vlans


# noinspection PyIncorrectDocstring
def svlan(items: Any = "", **kwargs) -> str:
    """**String VLAN IDs** - Sorting VLANs and removing duplicates
    :param items: Range of VLANs, can be unsorted and with duplicates,
        *str, List[int], List[str]*
    :param bool verbose: True - all VLAN IDs in verbose mode: [1, 2, ..., 65535],
                         False - all VLAN IDs in brief mode: [-1] (reduces RAM usage),
                         by default False
    :param bool all: True - Returns all VLAN IDs: "1-4094"
    :param splitter: Separator character between items, by default ","
    :param range_splitter: Separator between min and max numbers in range, by default "-"
    :param platform: Set `splitter` and `range_splitter` to platform specific values
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
    kwargs = _update_splitters(**kwargs)
    if h.is_all(**kwargs):
        return _replace_range_splitter(ALL_VLANS_S, **kwargs)
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = ",".join(h.lstr(h.remove_brief_items(items)))
            range_o: Range = parse_range(items_)
            _check_vlans(range_o.numbers())
            return _replace_range_splitter(ALL_VLANS_S, **kwargs)

    range_o = parse_range(items, **kwargs)
    _check_vlans(range_o.numbers())
    return str(range_o)


# ============================= helpers ==============================

def _check_vlans(items: LInt) -> bool:
    """Checks VLAN IDs
    :param items: VLAN IDs
    :return: True if all items are in the valid VLAN range 1...4094
    :raises ValueError: If on of item is outside valid range
    """
    if invalid_vlan := [i for i in items if i < MIN_VLAN or i > MAX_VLAN]:
        raise ValueError(f"{invalid_vlan=}, expected in range 1...4094")
    return True


def _replace_range_splitter(item: str, **kwargs) -> str:
    """Replaces "-" to range_splitter specified in kwargs"""
    range_splitter = kwargs.get("range_splitter") or ""
    if not range_splitter:
        return item
    item = item.replace("-", range_splitter)
    return item


def _update_splitters(**kwargs):
    """Updates `splitter` and `range_splitter` by `platform`
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
