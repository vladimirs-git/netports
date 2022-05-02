"""
**Interface4** - An object of interface name that can contain up to 4 indexes.
Useful for the interfaces strings by index (not by alphabetic).
"""
import re
from functools import total_ordering

from netports.types_ import TStr5


@total_ordering
class Interface4:
    """Interface"""

    def __init__(self, line: str = "", splitter: str = ",./:"):
        """Interface.
        :param line: Interface name that can contain up to 4 indexes.
        :param splitter: Separator characters between indexes. By default ",./:".
        """
        self.splitter = splitter
        self.line = line

    def __str__(self):
        return self.line

    def __repr__(self):
        return f"{self.__class__.__name__}({self.line!r})"

    def __hash__(self) -> int:
        return hash((self.id0, self.id1, self.id2, self.id3, self.id4))

    def __eq__(self, other) -> bool:
        """== equality"""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """< less than"""
        if self.__class__ == other.__class__:
            if self.id0 != other.id0:
                return self.id0 < other.id0
            if self.id1 != other.id1:
                return self.id1 < other.id1
            if self.id2 != other.id2:
                return self.id2 < other.id2
            if self.id3 != other.id3:
                return self.id3 < other.id3
            return self.id4 < other.id4
        return False

    # =========================== property ===========================

    @property
    def line(self) -> str:
        """Interface line"""
        return self._line

    @line.setter
    def line(self, line: str) -> None:
        if not isinstance(line, str):
            raise TypeError(f"{line=} {str} expected")
        items: TStr5 = self._parse_interface(line)
        self._id0 = items[0]
        self._id1 = int(items[1]) if items[1] else 0
        self._id2 = int(items[2]) if items[2] else 0
        self._id3 = int(items[3]) if items[3] else 0
        self._id4 = int(items[4]) if items[4] else 0
        self._line = line

    @property
    def id0(self) -> str:
        """Interface name. Line without *int* indexes"""
        return self._id0

    @property
    def id1(self) -> int:
        """Interface 1st index"""
        return self._id1

    @property
    def id2(self) -> int:
        """Interface 2nd index"""
        return self._id2

    @property
    def id3(self) -> int:
        """Interface 3rd index"""
        return self._id3

    @property
    def id4(self) -> int:
        """Interface 4th index"""
        return self._id4

    @property
    def name(self) -> str:
        """Interface name. Line without 1st part"""
        return re.sub(r"^interface\s+", "", self.line)

    @property
    def splitter(self) -> str:
        """Separator characters between indexes"""
        return self._line

    @splitter.setter
    def splitter(self, splitter: str) -> None:
        if not isinstance(splitter, str):
            raise TypeError(f"{splitter=} {str} expected")
        self._splitter = splitter

    # =========================== helpers ============================

    def _parse_interface(self, intf: str) -> TStr5:
        """Parse interface to name and indexes.
        :param intf: Interface that has up to 4 indexes as <str>.
        :return: split name and indexes
        Example:
            intf: "interface Ethernet1/2/3.4"
            return: ("interface Ethernet", 1, 2, 3, 4)
        """
        intf_ = intf
        for splitter in self._splitter:
            intf_ = intf_.replace(splitter, ",")

        name = r"([a-zA-Z\-\s]+)*"
        id1 = r"(\d+)*"
        id2 = r"(?:,)*(\d+)*"
        pattern = f"{name}{id1}{id2}{id2}{id2}"
        parsed: TStr5 = (re.findall(pattern, intf_) or [("", "", "", "", "")])[0]
        return parsed
