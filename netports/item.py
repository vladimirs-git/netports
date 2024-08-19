"""Item, element of Range."""

import re
from functools import total_ordering
from typing import List

from netports.exceptions import NetportsValueError


@total_ordering
class Item:
    """Item, element of Range."""

    def __init__(self, line: str):
        """Init Item.

        :param line: Item in str format.
        :type line: str

        :example:
            item = Item("1-3")
            item.line == "1-3"
            item.min == 1
            item.max == 3
            item.range == range(1, 3)
        """
        self.line = line

    def __str__(self):
        return self.line

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.line!r})"

    def __hash__(self) -> int:
        return hash((self.min, self.max))

    def __eq__(self, other) -> bool:
        """== equality."""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """< less than."""
        if self.__class__ == other.__class__:
            if self.min != other.min:
                return self.min < other.min
            return self.max < other.max
        return self.line < str(other)

    # =========================== property ===========================

    @property
    def line(self):
        """Item in str format."""
        return self._line

    @line.setter
    def line(self, line: str) -> None:
        if not re.match(r"\d+(-\d+)?$", line):
            raise NetportsValueError(f"{line=}, expected range")
        items = line.split("-")
        self._min = int(items[0])
        self._max = self._min if len(items) == 1 else int(items[1])
        if self.min > self.max:
            raise NetportsValueError(f"{self.max=} < {self.min=}")
        self._line = line

    @property
    def min(self):
        """First int in range."""
        return self._min

    @property
    def max(self):
        """Last int in range."""
        return self._max

    @property
    def range(self):
        """Item in *range* format."""
        return range(self.min, self.max + 1)


LItem = List[Item]
