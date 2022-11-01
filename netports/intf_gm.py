"""IntfGM - Interfaces Group Manager"""
from netports.intf import ULIntf, LIntf, Intf, LStr
from netports.range import Range
from netports.types_ import DSStr


class IntfGM:
    """IntfGM - Interfaces Group Manager"""

    def __init__(self, items):
        """IntfGM
        :param items: List of Interfaces
        :type items: str, List[str], Intf, List[Intf]
        """
        self.items = items

    def __repr__(self):
        name = self.__class__.__name__
        items = len(self.items)
        return f"<{name}: {items=}>"

    # =========================== property ===========================

    @property
    def items(self) -> LIntf:
        """Interface line"""
        return self._items

    @items.setter
    def items(self, items: ULIntf) -> None:
        if not items:
            _items = []
        elif isinstance(items, (str, Intf)):
            _items = [items]
        elif isinstance(items, (list, set, tuple)):
            _items = list(items)
        else:
            raise TypeError(f"{items=} {list} expected")

        items_: LIntf = []
        for item in _items:
            if isinstance(item, Intf):
                items_.append(item)
            elif isinstance(item, str):
                items_.append(Intf(item))
            else:
                raise TypeError(f"{item=} {str} expected")
        self._items = sorted(items_)

    # =========================== methods ===========================

    def ranges(self, fmt: str = "long") -> LStr:
        """Convert interfaces names to shorted range notation
        :param fmt: Format option
            "cisco" - Cisco compatible format  # todo
            "long"  - Long names: ["interface Ethernet1/1-3"]
            "short" - Short names: ["Eth1/1/1-3"]
        :type: str

        :return: Interfaces range notation
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
        """Convert interfaces names to long lines
        :example:
            intfs = ["interface Ethernet1/1", "interface Ethernet1/2", "interface Ethernet1/3"]
            intf_gm = IntfGM(intfs)
            intf_gm.ranges() -> ["interface Ethernet1/1-3"]
        """
        items = sorted(self.items)

        data: DSStr = {}
        for intf in items:
            idx = intf.last_idx()
            part = intf.part(idx)
            data[part] = set()

        for intf in items:
            idx = intf.last_idx()
            part_ = intf.part(idx)
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
        """Convert interfaces names to short lines
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

def intfrange(items: LStr, fmt: str = "long") -> LStr:
    """Convert interfaces names to shorted range notation
    :param items: List of interfaces
    :type items: List[str]

    :param fmt: Format option:
        "long"  - Long names: ["interface Ethernet1/1-3"]
        "short" - Short names: ["Eth1/1/1-3"]
    :type: str

    :return: Interface ranges
    :rtype: List[str]

    :example:
        ranges(["Ethernet1/1", "Ethernet1/2", "Ethernet1/3"]) -> ["Ethernet1/1-3"]
    """
    intf_gm = IntfGM(items)
    ranges_ = intf_gm.ranges(fmt=fmt)
    return ranges_
