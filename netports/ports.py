"""Ports"""

import re
from typing import Any

from netports import helpers as h
from netports.ranges import Ranges
from netports.static import RANGE_SPLITTER, SPLITTER
from netports.types_ import LStr, LInt


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
def inumbers(items: Any, **kwargs) -> LInt:
    """**integer numbers** - Sort numbers and remove duplicates.
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
    return ranges_.numbers


# noinspection PyIncorrectDocstring
def snumbers(items: Any, **kwargs) -> str:
    """**string numbers** - Sort numbers and remove duplicates.
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
