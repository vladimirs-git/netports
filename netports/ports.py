"""Ports"""

import re
from typing import Any

from netports import helpers as h
from netports.range import Range
from netports.static import RANGE_SPLITTER, SPLITTER
from netports.types_ import LStr, LInt


# noinspection PyIncorrectDocstring
def parse_range(line: str, **kwargs) -> Range:
    """Parses range from line. Removes white spaces considering splitters.
    Sort numbers and removes duplicates.
    ::
        :param line: Range of numbers, can be unsorted and with duplicates,
        :type line: str, List[int], List[str]

        :param splitter: Separator character between items (default ",")
        :type splitter: str

        :param range_splitter: Separator between min and max numbers in range (default "-")
        :type range_splitter: str

        :return: *Range* object of unique sorted numbers
        :rtype: Range

        :example: Remove duplicates and sort range of numbers
            parse_range("3-5,1,3-5,1") -> Range("1,3-5")
    """
    splitter = str(kwargs.get("splitter") or SPLITTER)
    range_splitter = str(kwargs.get("range_splitter") or RANGE_SPLITTER)
    regex = r"(\s+)?{}(\s+)?".format(range_splitter)
    items_: LStr = h.lstr(line)
    items_ = [re.sub(regex, range_splitter, s) for s in items_]
    items_ = [s.replace(range_splitter, "__range__") for s in items_]
    items_ = [s.replace(splitter, "__splitter__") for s in items_]
    items_ = ["".join(s.split()) for s in items_ if s]
    items_ = [s for s in items_ if s]
    items_ = [s.replace("__splitter__", splitter) for s in items_]
    items_ = [s.replace("__range__", range_splitter) for s in items_]
    line_ = splitter.join(items_)
    return Range(items=line_, splitter=splitter, range_splitter=range_splitter)


# noinspection PyIncorrectDocstring
def inumbers(items: Any, **kwargs) -> LInt:
    """Sort integer numbers and removes duplicates
    ::
        :param items: Range of numbers, can be unsorted and with duplicates
        :type items: str, List[int], List[str]

        :param splitter: Separator character between items (default ",")
        :type splitter: str

        :param range_splitter: Separator between min and max numbers in range (default "-")
        :type range_splitter: str

        :return: *List[int]* of unique sorted numbers
        :rtype: List[int

        :example: Converts *List[int]* to *List[int]* and removes duplicates
            inumbers([5, 5, 3, 4, 1]) -> [1, 3, 4, 5]

        :example: Converts *List[int]* to *List[int]* and removes duplicates
            inumbers("1, 7-9, 3 - 5") -> [1, 3, 4, 5, 7, 8, 9]
    """
    range_o: Range = parse_range(items, **kwargs)
    return range_o.numbers()


# noinspection PyIncorrectDocstring
def snumbers(items: Any, **kwargs) -> str:
    """Sort string numbers and removes duplicates
    ::
        :param items: Range of numbers, can be unsorted and with duplicates
        :type items: str, List[int], List[str]

        :param splitter: Separator character between items (default ",")
        :type splitter: str

        :param range_splitter: Separator between min and max numbers in range (default "-")
        :type range_splitter: str

        :return: *str* of unique sorted numbers
        :rtype: str

        :example: Converts *List[int]* to *str* and removes duplicates
            snumbers([5, 5, 3, 4, 1]) -> "1,3-5"

        :example: Converts *str* to *str* and removes duplicates
            snumbers("1, 7-9, 3 - 5") -> "1,3-5,7-9"
    """
    range_o: Range = parse_range(items, **kwargs)
    return str(range_o)
