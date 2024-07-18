"""An object of interface name, that can contain up to 6 indexes."""
import re
from functools import total_ordering
from typing import List, Optional, Set, Tuple, Union

from netports import intf_map, helpers as h
from netports.exceptions import NetportsValueError
from netports.static import DEVICE_TYPES
from netports.types_ import T5Str, LStr, SStr, DStr, LT2Str, T7Str

SPLITTER = ",./:"


@total_ordering
class Intf:
    """An object of interface name, that can contain up to 6 indexes."""

    def __init__(self, line: str = "", **kwargs):
        """Init Intf.

        :param line: Interface name that can contain up to 4 indexes
        :type line: str
        :param device_type: Netmiko device type (default "")
        :type device_type: str
        :param splitter: Separator of characters between indexes (default ",./:")
        :type splitter: str
        """
        self._device_type = self._init_device_type(**kwargs)
        self._splitter = str(kwargs.get("splitter") or SPLITTER)
        self._line = self._init_line(line)

    def __str__(self):
        """__str__."""
        return self.line

    def __repr__(self):
        """__repr__."""
        return f"{self.__class__.__name__}({self.line!r})"

    def __hash__(self) -> int:
        """__hash__."""
        return hash((self.id0, self.id1, self.id2, self.id3, self.id4, self.id5, self.id6))

    def __eq__(self, other) -> bool:
        """== equality."""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """< less than."""
        if self.__class__ == other.__class__:
            if self.id0 != other.id0:
                return self.id0 < other.id0
            if self.id1 != other.id1:
                return self.id1 < other.id1
            if self.id2 != other.id2:
                return self.id2 < other.id2
            if self.id3 != other.id3:
                return self.id3 < other.id3
            if self.id4 != other.id4:
                return self.id4 < other.id4
            if self.id5 != other.id5:
                return self.id5 < other.id5
            return self.id6 < other.id6
        return False

    # =========================== property ===========================

    @property
    def delimiters(self) -> T5Str:
        """Interface all delimiters."""
        return self._dels

    @property
    def id0(self) -> str:
        """Interface name. Line without IDs.

        :example:
            Intf("interface Ethernet1/2/3.4").id0 -> "interface Ethernet"
        """
        return self._ids[0]

    @property
    def id1(self) -> int:
        """Interface 1st ID.

        :example:
            Intf("interface Ethernet1/2/3.4").id1 -> 1
        """
        return int(self._ids[1]) if self._ids[1] else 0

    @property
    def id2(self) -> int:
        """Interface 2nd ID.

        :example:
            Intf("interface Ethernet1/2/3.4").id2 -> 2
        """
        return int(self._ids[2]) if self._ids[2] else 0

    @property
    def id3(self) -> int:
        """Interface 3rd ID.

        :example:
            Intf("interface Ethernet1/2/3.4") -> 3
        """
        return int(self._ids[3]) if self._ids[3] else 0

    @property
    def id4(self) -> int:
        """Interface 4th ID.

        :example:
            Intf("interface Ethernet1/2/3.4").id4 -> 4
        """
        return int(self._ids[4]) if self._ids[4] else 0

    @property
    def id5(self) -> int:
        """Interface 5th ID.

        :example:
            Intf("interface Ethernet1/2/3/4.5").id5 -> 5
        """
        return int(self._ids[5]) if self._ids[5] else 0

    @property
    def id6(self) -> int:
        """Interface 6th ID.

        :example:
            Intf("interface Ethernet1/2/3/4/5.6").id6 -> 6
        """
        return int(self._ids[6]) if self._ids[6] else 0

    @property
    def ids(self) -> T7Str:
        """Interface all IDs.

        :example:
            Intf("interface Ethernet1/2/3.4").ids ->
                "interface Ethernet", "1", "2", "3", "4", "", "")
        """
        return self._ids

    @property
    def line(self) -> str:
        """Interface line.

        :example:
            Intf("interface Ethernet1/2/3.4").line -> "interface Ethernet1/2/3.4"
        """
        return self._line

    @property
    def name(self) -> str:
        """Interface name with IDs.

        :example:
            Intf("interface Ethernet1/2/3.4").name -> "Ethernet1/2/3.4"
        """
        return re.sub(r"^interface(\s+)?", "", self.line)

    @property
    def device_type(self) -> str:
        """Netmiko device type."""
        return self._device_type

    @property
    def splitter(self) -> str:
        """Separator of characters between indexes."""
        return self._splitter

    # =========================== methods ============================

    def all_names(self) -> LStr:
        """All variants of names: long, short, upper-case, lover-case.

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
        results: SStr = set()

        names_: LStr = [self.line, self.name, self.name_full(), self.name_long(), self.name_short()]
        names_ = h.no_dupl(names_)
        for name_ in names_:
            results.add(name_)
            if not name_.startswith("interface "):
                name_ = f"interface {name_}"
                results.add(name_)

        intf_map_upper: DStr = intf_map.short_to_long(self._device_type)
        intf_map_lower: DStr = intf_map.short_to_long(self._device_type, key_lower=True)
        names: LStr = [self.name, self.name_short()]
        names = h.no_dupl(names)
        for name in names:
            intf_o = Intf(line=name, device_type=self.device_type)
            for id0_short, intf_map_d in [
                (intf_o.id0, intf_map_upper),
                (intf_o.id0.lower(), intf_map_lower),
            ]:
                if id0_long := intf_map_d.get(id0_short) or "":
                    name_long = intf_o.line.replace(id0_short, id0_long, 1)
                    results.add(name_long)
                    if not name_long.startswith("interface "):
                        results.add(f"interface {name_long}")

        results.update([s.lower() for s in results])

        results_: LStr = sorted(results)
        results_.sort(key=len, reverse=True)

        if self.device_type == "hp_procurve":
            if digits := [s for s in results if s.isdigit()]:
                names = [f"interface 1/{s}" for s in digits]
                results_.extend(names)
        return results_

    def last_idx(self) -> int:
        """Index of last ID in interface line.

        :example:
            Intf("interface Ethernet1/2/3.4").last_idx() -> 4
        """
        ids = self._ids[1:]
        return len([s for s in ids if s])

    def name_base(self) -> str:
        """Interface base name without IDs.

        :example:
            Intf("interface Ethernet1/2").name_base() -> "Ethernet"
        """
        return self.id0.replace("interface", "", 1).strip()

    def name_full(self) -> str:
        """Interface long name with IDs and with interface keyword.

        :example:
            Intf("Eth1/2").name_full() -> "interface Ethernet1/2"
        """
        name = self.name_long()
        if not name.startswith("interface"):
            name = " ".join([s for s in ("interface", name) if s])
        return name

    def name_long(self) -> str:
        """Interface long name with IDs and without interface keyword.

        :example:
            Intf("Eth1/2").name_long() -> "Ethernet1/2"
        """
        id0 = self.id0.lower()
        if id0.startswith("interface"):
            id0 = re.sub(r"^interface(\s+)?", "", id0, re.I)

        intf_map_short: DStr = intf_map.short_to_long(self._device_type, key_lower=True)
        for short_lower, long_upper in intf_map_short.items():
            if id0 == short_lower:
                id0 = long_upper
                break
        else:
            intf_map_long: DStr = intf_map.long_to_long(self._device_type, key_lower=True)
            for long_lower, long_upper in intf_map_long.items():
                if id0 == long_lower:
                    id0 = long_upper
                    break

        id1 = self.part_after(idx=0)
        name = f"{id0}{id1}"
        return name.strip()

    def name_short(self, replace: LT2Str = None) -> str:
        """Interface short name with IDs.

        :param replace: Replace the default short name with the first one
            that matches in the list of the `replace` argument.
        :return: Interface short name.

        :example:
            Intf("interface FastEthernet1/2").name_short() -> "Fa1/2"
            Intf("interface FastEthernet1/2").name_short(replace=[("Fa", "Eth")]) -> "Eth1/2"
        """
        id0 = self.id0.lower()
        if id0.startswith("interface"):
            id0 = re.sub(r"^interface(\s+)?", "", id0, re.I)

        intf_map_l2s: DStr = intf_map.long_to_short(self._device_type, key_lower=True)
        for long_lower, short_upper in intf_map_l2s.items():
            if id0 == long_lower:
                id0 = short_upper
                break
        else:
            intf_map_s2s: DStr = intf_map.short_to_short(self._device_type, key_lower=True)
            for short_lower, short_upper in intf_map_s2s.items():
                if id0 == short_lower:
                    id0 = short_upper
                    break

        if replace:
            for before, after in replace:
                if id0 == before:
                    id0 = after
                    break

        id1 = self.part_after(idx=0)
        name = f"{id0}{id1}"
        return name.strip()

    def part_after(self, idx: int, splitter=True) -> str:
        """Interface part after interested ID.

        :param idx: Interface index.
        :param splitter: True - Include splitter from edge, False - Skip splitter from edge.
        :return: Part of the interface name after specified interface index.

        :example:
            intf = Intf("Ethernet1/2/3.4")
            intf.part_after(0) -> "1/2/3.4"
            intf.part_after(1) -> "2/3.4"
            intf.part_after(2) -> "/3.4"
            intf.part_after(3) -> ".4"
            intf.part_after(2, splitter=False) -> "3.4"
        """
        if idx >= 6:
            return ""

        parts = self._ids[6]
        if idx == 5:
            if splitter:
                return self._dels[4] + parts
            return parts

        parts = self._ids[5] + self._dels[4] + parts
        if idx == 4:
            if splitter:
                return self._dels[3] + parts
            return parts

        parts = self._ids[4] + self._dels[3] + parts
        if idx == 3:
            if splitter:
                return self._dels[2] + parts
            return parts

        parts = self._ids[3] + self._dels[2] + parts
        if idx == 2:
            if splitter:
                return self._dels[1] + parts
            return parts

        parts = self._ids[2] + self._dels[1] + parts
        if idx == 1:
            if splitter:
                return self._dels[0] + parts
            return parts

        parts = self._ids[1] + self._dels[0] + parts
        if idx == 0:
            return parts

        parts = self._ids[0] + parts
        return parts

    def part_before(self, idx: int, splitter=True) -> str:
        """Interface part before interested ID.

        :param idx: Interface index.
        :param splitter: True - Include splitter from edge, False - Skip splitter from edge.
        :return: Part of the interface name before specified interface index.

        :example:
            intf = Intf("Ethernet1/2/3.4")
            intf.part_before(2) -> "Ethernet1/"
            intf.part_before(3) -> "Ethernet1/2/"
            intf.part_before(3, splitter=False) -> "Ethernet1/2"
        """
        if idx <= 0:
            return ""

        parts = self._ids[0]
        if idx == 1:
            return parts

        parts += self._ids[1]
        if idx == 2:
            if splitter:
                return parts + self._dels[0]
            return parts

        parts += self._dels[0] + self._ids[2]
        if idx == 3:
            if splitter:
                return parts + self._dels[1]
            return parts

        parts += self._dels[1] + self._ids[3]
        if idx == 4:
            if splitter:
                return parts + self._dels[2]
            return parts

        parts += self._dels[2] + self._ids[4]
        if idx == 5:
            if splitter:
                return parts + self._dels[3]
            return parts

        parts += self._dels[3] + self._ids[5]
        if idx == 6:
            if splitter:
                return parts + self._dels[4]
            return parts

        return self._line

    # =========================== helpers ============================

    def _get_ids(self) -> T7Str:
        """Split interface line to name and IDs.

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
        pattern = f"{name}{id1}{id2}{id2}{id2}{id2}{id2}"
        ids: T7Str = (re.findall(pattern, intf) or [("", "", "", "", "", "", "")])[0]
        return ids

    def _get_delimiters(self) -> T5Str:
        """Split interface line to splitters of IDs.

        :example:
            self.line: "interface Ethernet1/2/3.4"
            return: ("/, "/", ".")
        """
        part1 = self._ids[0] + self._ids[1]
        len1 = len(part1)
        delim1 = self._line[len1 : len1 + 1]

        part2 = part1 + delim1 + self._ids[2]
        len2 = len(part2)
        delim2 = self._line[len2 : len2 + 1]

        part3 = part2 + delim2 + self._ids[3]
        len3 = len(part3)
        delim3 = self._line[len3 : len3 + 1]

        part4 = part3 + delim3 + self._ids[4]
        len4 = len(part4)
        delim4 = self._line[len4 : len4 + 1]

        part5 = part4 + delim4 + self._ids[5]
        len5 = len(part5)
        delim5 = self._line[len5 : len5 + 1]
        return delim1, delim2, delim3, delim4, delim5

    def _init_line(self, line: str) -> str:
        """Init Interface line"""
        if not isinstance(line, str):
            raise TypeError(f"{line=} {str} expected")
        self._line = line
        self._ids: T7Str = self._get_ids()
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
            self._dels[3],
            self._ids[5],
            self._dels[4],
            self._ids[6],
        ]
        return "".join(items)

    @staticmethod
    def _init_device_type(**kwargs) -> str:
        """Init Netmiko device type.

        :return: Netmiko device type.
        :raises NetportsValueError: if the device type is unknown.
        """
        device_type = str(kwargs.get("device_type") or "")
        expected = ["", *DEVICE_TYPES]
        if device_type not in expected:
            raise NetportsValueError(f"{device_type=} {expected=}")
        return device_type


LIntf = List[Intf]
SIntf = Set[Intf]
TIntf = Tuple[Intf]
ULIntf = Optional[Union[str, LStr, Intf, LIntf]]
