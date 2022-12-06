"""An object of interface name, that can contain up to 4 indexes.
Sorts the interfaces by indexes (not by alphabetic).
"""
import re
from functools import cached_property, total_ordering
from typing import List, Optional, Set, Tuple, Union

from netports.intf_name_map import long_to_short_lower, short_to_long, short_to_long_lower
from netports.types_ import T3Str, T5Str, LStr, SStr

SPLITTER = ",./:"


@total_ordering
class Intf:
    """An object of interface name, that can contain up to 4 indexes.
    Sorts the interfaces by indexes (not by alphabetic).
    """

    def __init__(self, line: str = "", **kwargs):
        """Intf
        ::
            :param line: Interface name that can contain up to 4 indexes
            :type line: str

            :param splitter: Separator characters between indexes, by default ",./:"
            :type splitter: str
        """
        self._splitter = str(kwargs.get("splitter") or SPLITTER)
        self._line = self._init_line(line)

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

    # ============================= init =============================

    def _init_line(self, line: str) -> str:
        """Init Interface line"""
        if not isinstance(line, str):
            raise TypeError(f"{line=} {str} expected")
        self._line = line
        self._ids: T5Str = self._get_ids()
        self._dels = self._get_delimiters()

        items = [
            self._ids[0],
            self._ids[1],
            self._dels[0],
            self._ids[2],
            self._dels[1],
            self._ids[3],
            self._dels[2],
            self._ids[4],
        ]
        return "".join(items)

    # =========================== property ===========================

    @property
    def delimiters(self) -> T3Str:
        """Interface all delimiters"""
        return self._dels

    @property
    def id0(self) -> str:
        """Interface name. Line without IDs
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.id0 -> "interface Ethernet"
        """
        return self._ids[0]

    @property
    def id1(self) -> int:
        """Interface 1st ID
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.id1 -> 1
        """
        return int(self._ids[1]) if self._ids[1] else 0

    @property
    def id2(self) -> int:
        """Interface 2nd ID
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.id2 -> 2
        """
        return int(self._ids[2]) if self._ids[2] else 0

    @property
    def id3(self) -> int:
        """Interface 3rd ID
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.id3 -> 3
        """
        return int(self._ids[3]) if self._ids[3] else 0

    @property
    def id4(self) -> int:
        """Interface 4th ID
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.id4 -> 4
        """
        return int(self._ids[4]) if self._ids[4] else 0

    @property
    def ids(self) -> T5Str:
        """Interface all IDs
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.ids -> "interface Ethernet", "1", "2", "3", "4")
        """
        return self._ids

    @property
    def line(self) -> str:
        """Interface line
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.line -> "interface Ethernet1/2/3.4"
        """
        return self._line

    @property
    def name(self) -> str:
        """Interface name with IDs
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.name -> "Ethernet1/2/3.4"
        """
        return re.sub(r"^interface\s+", "", self.line)

    @cached_property
    def name_short(self) -> str:
        """Interface short name with IDs
        ::
            :example:
                intf = Intf("interface FastEthernet1/2")
                intf.name_short() -> "Fa1/2"
        """
        name = self.name.lower()
        for long, short in long_to_short_lower.items():
            if name.startswith(long):
                return name.replace(long, short)
        return name

    # =========================== methods ============================

    def last_idx(self) -> int:
        """Index of last ID in interface line
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.last_idx() -> 4
        """
        ids = self._ids[1:]
        return len([s for s in ids if s])

    def all_names(self) -> LStr:
        """All variants of names: long, short, upper-case, lover-case
        ::
            :example:
                Intf("Eth1/2").names() -> [
                    "interface Ethernet1/2",
                    "interface ethernet1/2",
                    "interface Eth1/2",
                    "interface eth1/2",
                    "Ethernet1/2",
                    "ethernet1/2",
                    "Eth1/2",
                    "eth1/2",
                ]
        """
        results: SStr = {self.line}
        results.add(self.name)
        results.add(self.name_short)

        for name in [self.name, self.name_short]:
            short_o = Intf(name)
            maps = [(short_o.id0, short_to_long), (short_o.id0.lower(), short_to_long_lower)]
            for id0_short, map_d in maps:
                if id0_long := map_d.get(id0_short):
                    name_long = short_o.line.replace(id0_short, id0_long, 1)
                    results.add(name_long)
                    results.add(f"interface {name_long}")

        results.update([s.lower() for s in results])
        results_: LStr = sorted(results)
        results_.sort(key=lambda s: len(s), reverse=True)
        return results_

    def part(self, idx: int) -> str:
        """Interface part before interested ID
        ::
            :example:
                intf = Intf("interface Ethernet1/2/3.4")
                intf.parts(2) -> "Ethernet1/"
        """
        if idx <= 0:
            return ""
        parts = self._ids[0]
        if idx == 1:
            return parts

        parts += self._ids[1] + self._dels[0]
        if idx == 2:
            return parts

        parts += self._ids[2] + self._dels[1]
        if idx == 3:
            return parts

        parts += self._ids[3] + self._dels[2]
        if idx == 4:
            return parts

        return self._line

    # =========================== helpers ============================

    def _get_ids(self) -> T5Str:
        """Splits interface line to name and IDs
        ::
            :example:
                self.line: "interface Ethernet1/2/3.4"
                return: ("interface Ethernet", "1", "2", "3", "4")
        """
        intf = self._line
        for splitter in self._splitter:
            intf = intf.replace(splitter, ",")

        name = r"([a-zA-Z\-\s]+)*"
        id1 = r"(\d+)*"
        id2 = r"(?:,)*(\d+)*"
        pattern = f"{name}{id1}{id2}{id2}{id2}"
        ids: T5Str = (re.findall(pattern, intf) or [("", "", "", "", "")])[0]
        return ids

    def _get_delimiters(self) -> T3Str:
        """Splits interface line to splitters of IDs
        ::
            :example:
                self.line: "interface Ethernet1/2/3.4"
                return: ("/, "/", ".")
        """
        part1 = self._ids[0] + self._ids[1]
        len1 = len(part1)
        delim1 = self._line[len1:len1 + 1]

        part2 = part1 + delim1 + self._ids[2]
        len2 = len(part2)
        delim2 = self._line[len2:len2 + 1]

        part3 = part2 + delim2 + self._ids[3]
        len3 = len(part3)
        delim3 = self._line[len3:len3 + 1]
        return delim1, delim2, delim3


LIntf = List[Intf]
SIntf = Set[Intf]
TIntf = Tuple[Intf]
ULIntf = Optional[Union[str, LStr, Intf, LIntf]]
