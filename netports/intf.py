"""Network interface representation with up to 6 numerical indices."""

import re
from functools import total_ordering
from typing import List, Optional, Set, Tuple, Union

from vhelpers import vlist

from netports import intf_map
from netports.exceptions import NetportsValueError
from netports.types_ import T5Str, LStr, SStr, DStr, T7Str, OLT2Str, OLStr

DEVICE_TYPES = [
    "cisco_ios",
    "cisco_nxos",
    "cisco_xr",
    "hp_comware",
    "hp_procurve",
]
SPLITTER = ",./:"


@total_ordering
class Intf:
    """Network interface representation with up to 6 numerical indices."""

    def __init__(self, line: str = "", **kwargs):
        """Initialize Intf.

        :param line: Interface name that can contain up to 4 indexes.
        :type line: str
        :param device_type: Netmiko device type (default "").
        :type device_type: str
        :param splitter: Separator of characters between indexes (default ",./:").
        :type splitter: str
        """
        self._device_type = _init_device_type(**kwargs)
        self._splitter = _init_splitter(**kwargs)
        self._ids: T7Str = self._init_ids(line)
        self._delimiters: T5Str = self._init_delimiters(line)
        self.line = self._init_line()

    def __repr__(self) -> str:
        """Representation of the object."""
        class_ = self.__class__.__name__
        return f"{class_}({self.line!r})"

    def __str__(self) -> str:
        """String representation."""
        return str(self.line)

    def __hash__(self) -> int:
        """Hash value of the object."""
        ids = (self.id0, self.id1, self.id2, self.id3, self.id4, self.id5, self.id6)
        return hash(ids)

    def __eq__(self, other) -> bool:
        """Check if two objects are equal.

        :param other: Another object to compare.
        :return: True if objects are equal, False otherwise.
        """
        if self.__class__ != other.__class__:
            return False
        return self.__hash__() == other.__hash__()

    def __lt__(self, other) -> bool:
        """Compare two objects.

        :param other: Another object to compare with.
        """
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
        return self._delimiters

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
        names_ = vlist.no_dupl(names_)
        for name_ in names_:
            results.add(name_)
            if not name_.startswith("interface "):
                name_ = f"interface {name_}"
                results.add(name_)

        intf_map_upper: DStr = intf_map.short_to_long(self._device_type)
        intf_map_lower: DStr = intf_map.short_to_long(self._device_type, key_lower=True)
        names: LStr = [self.name, self.name_short()]
        names = vlist.no_dupl(names)
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

    def name_short(self, replace: OLT2Str = None) -> str:
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
                return self._delimiters[4] + parts
            return parts

        parts = self._ids[5] + self._delimiters[4] + parts
        if idx == 4:
            if splitter:
                return self._delimiters[3] + parts
            return parts

        parts = self._ids[4] + self._delimiters[3] + parts
        if idx == 3:
            if splitter:
                return self._delimiters[2] + parts
            return parts

        parts = self._ids[3] + self._delimiters[2] + parts
        if idx == 2:
            if splitter:
                return self._delimiters[1] + parts
            return parts

        parts = self._ids[2] + self._delimiters[1] + parts
        if idx == 1:
            if splitter:
                return self._delimiters[0] + parts
            return parts

        parts = self._ids[1] + self._delimiters[0] + parts
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
                return parts + self._delimiters[0]
            return parts

        parts += self._delimiters[0] + self._ids[2]
        if idx == 3:
            if splitter:
                return parts + self._delimiters[1]
            return parts

        parts += self._delimiters[1] + self._ids[3]
        if idx == 4:
            if splitter:
                return parts + self._delimiters[2]
            return parts

        parts += self._delimiters[2] + self._ids[4]
        if idx == 5:
            if splitter:
                return parts + self._delimiters[3]
            return parts

        parts += self._delimiters[3] + self._ids[5]
        if idx == 6:
            if splitter:
                return parts + self._delimiters[4]
            return parts

        return self.line

    # =========================== helpers ============================

    def _init_line(self) -> str:
        """Parse Interface line.

        :return: Interface line with IDs and delimiters.
        """
        items: LStr = [
            self._ids[0],
            self._ids[1],
            self._delimiters[0],
            self._ids[2],
            self._delimiters[1],
            self._ids[3],
            self._delimiters[2],
            self._ids[4],
            self._delimiters[3],
            self._ids[5],
            self._delimiters[4],
            self._ids[6],
        ]
        items = [s for s in items if s]
        return "".join(items)

    def _init_ids(self, intf: str) -> T7Str:
        """Split interface line to name and IDs.

        :param intf: Interface line to split.
        :example:
            self.line: "interface Ethernet1/2/3.4"
            return: ("interface Ethernet", "1", "2", "3", "4")
        """
        for splitter in self._splitter:
            intf = intf.replace(splitter, ",")

        name = r"([a-zA-Z\-\s]+)*"
        id1 = r"(\d+)*"
        id2 = r"(?:,)*(\d+)*"
        pattern = f"{name}{id1}{id2}{id2}{id2}{id2}{id2}"
        ids: T7Str = (re.findall(pattern, intf) or [("", "", "", "", "", "", "")])[0]
        return ids

    def _init_delimiters(self, intf: str) -> T5Str:  # pylint: disable=too-many-locals
        """Split interface line to splitters of IDs.

        :param intf: Interface line to split.
        :return: Tuple of up to 5 delimiters between IDs.
        :example:
            self.line: "interface Ethernet1/2/3.4"
            return: ("/", "/", ".", "", "")
        """
        part1 = self._ids[0] + self._ids[1]
        len1 = len(part1)
        delim1 = intf[len1 : len1 + 1]

        part2 = part1 + delim1 + self._ids[2]
        len2 = len(part2)
        delim2 = intf[len2 : len2 + 1]

        part3 = part2 + delim2 + self._ids[3]
        len3 = len(part3)
        delim3 = intf[len3 : len3 + 1]

        part4 = part3 + delim3 + self._ids[4]
        len4 = len(part4)
        delim4 = intf[len4 : len4 + 1]

        part5 = part4 + delim4 + self._ids[5]
        len5 = len(part5)
        delim5 = intf[len5 : len5 + 1]
        return delim1, delim2, delim3, delim4, delim5


LIntf = List[Intf]
SIntf = Set[Intf]
TIntf = Tuple[Intf]
ULIntf = Optional[Union[str, LStr, Intf, LIntf]]


# ============================ functions =============================


def is_port_base(port: str, required: OLStr = None, ignore: OLStr = None) -> bool:
    """Check if the port has one of the required base, skipping base that are in the ignore list.

    :param port: Port name that need to check.
    :type port: str

    :param required: Required base names (without ID),
        one of which should match with port base name.
    :type required: List[str]

    :param ignore: Base names to ignore.
    :type ignore: List[str]

    :return: True - if port base name matches with required, False - otherwise.
    :rtype: bool
    """
    base = Intf(port).id0
    if ignore:
        if base in ignore:
            return True
    if required:
        if base in required:
            return True
    return False


def sort_names(names: LStr, reverse: bool = False) -> LStr:
    """Sort interface names.

    :param names: Interface names that need to be sorted.
    :type names: List[str]

    :param reverse: True - descending, False - ascending, default is False.
    :type reverse: bool

    :return: Sorted interface names.
    :rtype: List[str]
    """
    intfs: LIntf = sorted([Intf(s) for s in names], reverse=reverse)
    return [o.line for o in intfs]


# ============================= helpers ==============================


def _init_device_type(**kwargs) -> str:
    """Validate Netmiko device type.

    :return: Device type.
    :raises NetportsValueError: if the device type is unsupported.
    """
    device_type = str(kwargs.get("device_type") or "")
    expected = ["", *DEVICE_TYPES]
    if device_type not in expected:
        raise NetportsValueError(f"{device_type=} {expected=}")
    return device_type


def _init_splitter(**kwargs) -> str:
    """Validate splitter between interface IDs.

    :return: Splitters pattern.
    """
    if splitter := str(kwargs.get("splitter") or ""):
        return splitter
    return SPLITTER
