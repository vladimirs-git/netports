"""IntfGM - Interfaces Group Manager."""
from vhelpers import vre

from netports.intf import ULIntf, LIntf, Intf, LStr
from netports.range import Range
from netports.types_ import DSStr


class IntfGM:
    """IntfGM - Interfaces Group Manager."""

    def __init__(self, items):
        """Init IntfGM

        :param items: List of Interfaces.
        :type items: str or List[str] or Intf or List[Intf]
        """
        self.items = items

    def __repr__(self):
        name = self.__class__.__name__
        items = len(self.items)
        return f"<{name}: {items=}>"

    # =========================== property ===========================

    @property
    def items(self) -> LIntf:
        """Interface lin."""
        return self._items

    @items.setter
    def items(self, items: ULIntf) -> None:
        if not items:
            _items = []
        elif isinstance(items, (list, set, tuple)):
            _items = list(items)
        else:
            _items = [items]

        items_: LIntf = []
        for item in _items:
            if isinstance(item, Intf):
                items_.append(item)
            else:
                item = str(item)
                items_.append(Intf(item))
        self._items = sorted(items_)

    # =========================== methods ===========================

    def ranges(self, fmt: str = "long") -> LStr:
        """Convert interfaces names to shorted range notation.

        :param fmt: Format option:
            "cisco" - Cisco compatible format
            "long"  - Long names: ["interface Ethernet1/1-3"]
            "short" - Short names: ["Eth1/1/1-3"]
        :type fmt: str

        :return: Interfaces range notation.
        :rtype: List[str]
        """
        if fmt == "long":
            return self._ranges__long()
        if fmt == "short":
            return self._ranges__short()
        expected = ["long", "short"]
        raise ValueError(f"{fmt=} {expected=}")

    # =========================== helpers ============================

    def _ranges__long(self) -> LStr:
        """Convert interfaces names to long lines.

        :example:
            intfs = ["interface Ethernet1/1", "interface Ethernet1/2", "interface Ethernet1/3"]
            intf_gm = IntfGM(intfs)
            intf_gm.ranges() -> ["interface Ethernet1/1-3"]
        """
        items = sorted(self.items)

        data: DSStr = {}
        for intf in items:
            idx = intf.last_idx()
            part = intf.part_before(idx)
            data[part] = set()

        for intf in items:
            idx = intf.last_idx()
            part_ = intf.part_before(idx)
            id_ = intf.ids[idx]
            data[part_].add(id_)

        ranges = []
        for key, ids in data.items():
            ids_ = [int(s) for s in ids]
            range_o = Range(ids_)
            for item in range_o.items:
                ranges.append(f"{key}{item}")
        return ranges

    def _ranges__short(self) -> LStr:
        """Convert interfaces names to short lines.

        :example:
            intfs = ["interface Ethernet1/1", "interface Ethernet1/2", "interface Ethernet1/3"]
            intf_gm = IntfGM(intfs)
            intf_gm.ranges() -> ["Eth1/1-3"]
        """
        long_intfs: LStr = self._ranges__long()
        short_intfs: LStr = []
        for long_intf in long_intfs:
            long_intf = long_intf.lower()
            intf_o = Intf(long_intf)
            name_short = intf_o.name_short()
            postfix = long_intf.replace(intf_o.line, "")
            short_intf = name_short + postfix
            short_intfs.append(short_intf)
        return short_intfs


# ============================ functions =============================

def generate_intfs(start: str, end: str, base: str = "") -> LIntf:
    """Generate list of Intf objects from start to end.

    :param start: First interface name in the range.
    :type start: str

    :param end: Last interface name in the range.
    :type end: str

    :param base: Prefix of the interface name that needs to be added to each interface.
    :type base: str

    :return: List of generated Intf objects.
    :rtype: List[Intf]

    :example:
        generate_intfs(start="1/1", end="1/3") -> [Intf("1/1"), Intf("1/2"), Intf("1/3")]
    """
    names: LStr = generate_names(start=start, end=end, base=base)
    intfs: LIntf = [Intf(s) for s in names]
    return intfs


def generate_names(start: str, end: str, base: str = "") -> LStr:
    """Generate list of interface names from start to end.

    :param start: First interface name in the range.
    :type start: str

    :param end: Last interface name in the range.
    :type end: str

    :param base: Prefix of the interface name that needs to be added to each interface.
    :type base: str

    :return: List of generated interface names.
    :rtype: List[str]

    :example:
        generate_names(start="Eth1/1", end="Eth1/3") -> ["Eth1/1", "Eth1/2", "Eth1/3"]
    """
    # start
    base_first, first = vre.find2(r"(.*?)(\d+)$", start)
    if not first:
        raise ValueError("Invalid parameter `start`, digit is expected.")
    # end
    base_last, last = vre.find2(r"(.*?)(\d+)$", end)
    if not last:
        raise ValueError("Invalid parameter `end`, digit is expected.")
    # base
    if base_first != base_last:
        raise ValueError(f"Invalid parameters `start` and `end`. The same base name is expected.")

    names: LStr = []

    for idx in range(int(first), int(last) + 1):
        name = f"{base}{base_first}{idx}"
        names.append(name)

    return names


def names_to_range(names: LStr, fmt: str = "long") -> str:
    """Join list of interface names to range.

    :param names: List of interface names.
    :type names: List[str]

    :param fmt: Format option:
        "long"  - Long names: ["interface Ethernet1/1-3"]
        "short" - Short names: ["Eth1/1/1-3"]
    :type fmt: str

    :return: Interface range.
    :rtype: str

    :example:
        names_to_range(["Ethernet1/1", "Ethernet1/2", "Ethernet1/3"], "long") -> "Ethernet1/1-3"
        names_to_range(["Ethernet1/1", "Ethernet1/2", "Ethernet1/3"], "short") -> "Eth1/1-3"
    """
    intf_gm = IntfGM(names)
    ranges = intf_gm.ranges(fmt=fmt)
    return ",".join(ranges)


def range_to_intfs(line: str, base: str = "") -> LIntf:
    """Split interface range to list of Intf objects.

    :param line: Range of interfaces that need to be split.
    :type line: str

    :param base: Prefix of the interface name that needs to be added to each interface.
    :type base: str

    :return: List of Intf objects.
    :rtype: List[Intf]

    :example:
        range_to_intfs("1/1-3,1/5") -> [Intf("1/1"), Intf("1/2"), Intf("1/3"), Intf("1/5")]
    """
    names: LStr = []

    splitter = "-"
    items: LStr = [s.strip() for s in line.split(",")]
    items = [s for s in items if s]

    for item in items:
        if item.find(splitter) == -1:
            names.append(item)
            continue

        first_last = item.split("-")
        if len(first_last) != 2:
            raise ValueError(f"Invalid range {item=}.")
        base_first, base_last = first_last

        if base_last.isdigit():
            last = base_last
            base1, first = vre.find2(r"^(.*?)(\d+)$", base_first)
        else:
            base1, first = vre.find2(r"^(.*?)(\d+)$", base_first)
            base2, last = vre.find2(r"^(.*?)(\d+)$", base_last)
            if base1 != base2:
                raise ValueError(f"Invalid range {item=}.")

        if not (first and last):
            raise ValueError(f"Invalid range {item=}.")

        for idx in range(int(first), int(last) + 1):
            name = f"{base1}{idx}"
            names.append(name)

    intfs: LIntf = sorted([Intf(f"{base}{s}") for s in set(names)])
    return intfs


def range_to_names(line: str, base: str = "") -> LStr:
    """Split interface range to list of interface names.

    :param line: Range of interfaces that need to be split.
    :type line: str

    :param base: Prefix of the interface name that needs to be added to each interface.
    :type base: str

    :return: List of interface names.
    :rtype: List[str]

    :example:
        range_to_names("1/1-3,1/5") -> ["1/1", "1/2", "1/3", "1/5"]
        range_to_names("1/1-1/3,1/5") -> ["1/1", "1/2", "1/3", "1/5"]
    """
    intfs: LIntf = range_to_intfs(line=line, base=base)
    return [o.line for o in intfs]
