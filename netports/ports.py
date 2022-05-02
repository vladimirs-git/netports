"""VLAN, TCP ports functions"""

import re
from typing import Any

from netports import helpers as h
from netports.ranges import Ranges, check_vlans_range, check_tcp_range
from netports.static import RANGE_SPLITTER, RANGE_SPLITTER_HPE, SPLITTER, SPLITTER_HPE
from netports.types_ import LStr, LInt


# ============================== ports ===============================

# noinspection PyIncorrectDocstring
def ranges(line: str, **kwargs) -> Ranges:
    """**range of numbers** - Sort numbers and remove duplicates.
    :param line: Range of numbers, can be unsorted and with duplicates.
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :return: Ranges *object* of unique sorted numbers.

    Example: Remove duplicates and sort range of numbers.
        line: "3-5,1,3-5,1"
        return: Ranges("1,3-5")
    """
    splitter = str(kwargs.get("splitter") or SPLITTER)
    range_splitter = str(kwargs.get("range_splitter") or RANGE_SPLITTER)
    regex = r"(\s+)?{}(\s+)?".format(range_splitter)
    items_: LStr = h.list_of_str(line)
    items_ = [re.sub(regex, range_splitter, s) for s in items_]
    items_ = [s.replace(range_splitter, "__range__") for s in items_]
    items_ = [s.replace(splitter, "__splitter__") for s in items_]
    items_ = ["".join(s.split()) for s in items_ if s]
    items_ = [s for s in items_ if s]
    items_ = [s.replace("__splitter__", splitter) for s in items_]
    items_ = [s.replace("__range__", range_splitter) for s in items_]
    line_ = splitter.join(items_)
    ranges_ = Ranges(line=line_, splitter=splitter, range_splitter=range_splitter)
    return ranges_


# noinspection PyIncorrectDocstring
def iports(items: Any, **kwargs) -> LInt:
    """**integer ports** - Sort numbers and remove duplicates.
    :param items: Range of numbers or *List[int]*, can be unsorted and with duplicates.
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :return: *List[int]* of unique sorted numbers.

    Example1: Convert *List[int]* to *List[int]* and remove duplicates.
        items: [5, 5, 3, 4, 1]
        return: [1, 3, 4, 5]

    Example2: Convert *List[int]* to *List[int]* and remove duplicates.
        items: "1, 7-9, 3 - 5"
        return: [1, 3, 4, 5, 7, 8, 9]
    """
    ranges_: Ranges = ranges(items, **kwargs)
    return ranges_.ports


# noinspection PyIncorrectDocstring
def sports(items: Any, **kwargs) -> str:
    """**string ports** - Sort numbers and remove duplicates.
    :param items: Range of numbers or *List[int]*, can be unsorted and with duplicates.
    :param splitter: Separator character between items. By default ",".
    :param range_splitter: Separator between min and max numbers in range. By default "-".
    :return: *str* of unique sorted numbers.

    Example1: Convert *List[int]* to <str> and remove duplicates.
        items: [5, 5, 3, 4, 1]
        return: "1,3-5"

    Example2: Convert <str> to <str> and remove duplicates.
        items: "1, 7-9, 3 - 5"
        return: "1,3-5,7-9"
    """
    ranges_: Ranges = ranges(items, **kwargs)
    return str(ranges_)


# =============================== tcp ================================

def itcp(items: Any) -> LInt:
    """**Integer TCP/UDP ports** - Sort numbers and remove duplicates.
    :param items: Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates.
    :return: *List[int]* of unique sorted TCP/UDP ports.
        Raise *ValueError* if TCP/UDP ports are outside valid range 1...65535.
    Example:
        items: "1,3-5"
        return: [1, 3, 4, 5]
    """
    ports: LInt = iports(items)
    check_tcp_range(ports=ports)
    return ports


def stcp(items: Any) -> str:
    """**String TCP/UDP ports** - Sort numbers and remove duplicates.
    :param items: Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates.
    :return: *str* of unique sorted TCP/UDP ports.
        Raise *ValueError* if TCP/UDP ports are outside valid range 1...65535.
    Example:
        items: [1, 3, 4, 5]
        return: "1,3-5"
    """
    ranges_: Ranges = ranges(items)
    check_tcp_range(ports=ranges_.ports)
    return str(ranges_)


# =============================== vlan ===============================

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
    vlans: LInt = iports(items, **kwargs)
    check_vlans_range(vlans=vlans)
    return vlans


def ivlan_hpe(items: Any) -> LInt:
    """**Integer VLAN IDs, for Hewlett Packard Enterprise** - Sort VLANs and remove duplicates.
    :param items: Range of VLANs or *List[int]*, can be unsorted and with duplicates.
    :return: *List[int]* of unique sorted VLANs, for Hewlett Packard Enterprise.
        Raise *ValueError* if VLANs are outside valid range 1...4094.
    Example:
        items: "1 3 to 5"
        return: [1, 3, 4, 5]
    """
    vlans: LInt = iports(items, splitter=SPLITTER_HPE, range_splitter=RANGE_SPLITTER_HPE)
    check_vlans_range(vlans=vlans)
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
    check_vlans_range(vlans=ranges_.ports)
    return str(ranges_)


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
    check_vlans_range(vlans=ranges_.ports)
    return str(ranges_)
