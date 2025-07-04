"""VLAN IDs."""

from typing import Any

from netports import Range
from netports import helpers as h
from netports.exceptions import NetportsValueError
from netports.ports import inumbers, parse_range
from netports.static import BRIEF_ALL_I, RANGE_SPLITTER, SPLITTER
from netports.types_ import LInt

MIN_VLAN = 1
MAX_VLAN = 4094
ALL_VLANS_L = list(range(MIN_VLAN, MAX_VLAN + 1))
ALL_VLANS_S = f"{MIN_VLAN}-{MAX_VLAN}"
SPLITTER_HPE = " "
RANGE_SPLITTER_HPE = " to "


# noinspection PyIncorrectDocstring
def ivlan(items: Any = "", **kwargs) -> LInt:
    """Sorting integer VLAN IDs and removing duplicates.

    :param items: Range of VLANs, can be unsorted and with duplicates.
    :type items: str or List[int] or List[str]

    :param verbose: True - all VLAN IDs in verbose mode: [1, 2, ..., 4094],
        False - all VLAN IDs in brief mode: [-1], to save RAM (default).
    :type verbose: bool

    :param all: True - Returns all VLAN IDs: [1, 2, ..., 4094], or [-1] for verbose=False.
    :type all: bool

    :param splitter: Separator character between items (default ",").
    :type splitter: str

    :param range_splitter: Separator between min and max numbers in range (default "-").
    :type range_splitter: str

    :param platform: Set `splitter` and `range_splitter` to platform specific values.
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :type platform: str

    :return: List[int] of unique sorted VLANs.
    :rtype: List[int]

    :raises NetportsValueError: if VLANs are outside valid range 1...4094.

    :example:
        ivlan("1,3-5") -> [1, 3, 4, 5]
    """
    if h.is_all(**kwargs):
        if h.is_brief(**kwargs):
            return [BRIEF_ALL_I]
        return ALL_VLANS_L.copy()
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = h.remove_brief_items(items)
            ports = inumbers(items_)
            check_vlans(ports)
            return [BRIEF_ALL_I]

    kwargs = _update_splitters(**kwargs)
    vlans: LInt = inumbers(items, **kwargs)
    check_vlans(vlans)

    if h.is_brief(**kwargs):
        if vlans == ALL_VLANS_L:
            return [BRIEF_ALL_I]
    return vlans


# noinspection PyIncorrectDocstring
def svlan(items: Any = "", **kwargs) -> str:
    """Sorting string VLANs and removing duplicates.

    :param items: Range of VLANs, can be unsorted and with duplicates.
    :type items str or List[int] or List[str]

    :param verbose: True - all VLAN IDs in verbose mode: [1, 2, ..., 4094],
        False - all VLAN IDs in brief mode: [-1], to save RAM (default).
    :type verbose: bool

    :param all: True - Returns all VLAN IDs: "1-4094".
    :type all: bool

    :param splitter: Separator character between items (default ",").
    :type splitter: str

    :param range_splitter: Separator between min and max numbers in range (default "-").
    :type range_splitter: str

    :param platform: Set `splitter` and `range_splitter` to platform specific values.
        platform    splitter    range_splitter  description
        ==========  ==========  ==============  ==========================
        "cisco"     ","         "-"             Cisco IOS
        "hpe"       " "         " to "          Hewlett Packard Enterprise
    :type platform: str

    :return: str of unique sorted VLANs.
    :rtype: str

    :raises NetportsValueError: if VLANs are outside valid range 1...4094.

    :example:
        svlan([1, 3, 4, 5]) -> "1,3-5"
    """
    kwargs = _update_splitters(**kwargs)
    if h.is_all(**kwargs):
        return _replace_range_splitter(ALL_VLANS_S, **kwargs)
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = ",".join(h.lstr(h.remove_brief_items(items)))
            range_o: Range = parse_range(items_)
            check_vlans(range_o.numbers())
            return _replace_range_splitter(ALL_VLANS_S, **kwargs)

    range_o = parse_range(items, **kwargs)
    check_vlans(range_o.numbers())
    return str(range_o)


# ============================= helpers ==============================


def _replace_range_splitter(item: str, **kwargs) -> str:
    """Replace "-" to range_splitter specified in kwargs."""
    range_splitter = kwargs.get("range_splitter") or ""
    if not range_splitter:
        return item
    item = item.replace("-", range_splitter)
    return item


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


# ============================= functions ==============================


def check_vlans(items: LInt) -> bool:
    """Check VLAN IDs.

    :param items: VLAN IDs.
    :return: True if all items are in the valid VLAN range 1...4094.
    :raises NetportsValueError: If on of item is outside valid range.
    """
    if invalid_vlan := [i for i in items if i < MIN_VLAN or i > MAX_VLAN]:
        raise NetportsValueError(f"{invalid_vlan=}, expected in range 1...4094")
    return True
