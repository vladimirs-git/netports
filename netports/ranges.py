"""Ranges"""

from functools import total_ordering

from netports.range import Range, LRange
from netports.static import SPLITTER, RANGE_SPLITTER
from netports.types_ import LStr, LInt, OInt, SInt, IInt


@total_ordering
class Ranges:
    """Ranges"""

    __slots__ = ("_line", "_ports", "splitter", "range_splitter", "_valid_chars")

    def __init__(self, line: str, splitter: str = SPLITTER, range_splitter: str = RANGE_SPLITTER):
        """Ranges.
        :param line: Range in <str> format.
        :param splitter: Separator character between numbers. By default ",".
        :param range_splitter: Separator between min and max digits in range. By default "-".
        """
        self.splitter = splitter
        self.range_splitter = range_splitter
        self._ports: LInt = []
        self.line = line

    def __str__(self):
        return self.line

    def __repr__(self):
        splitter = self.splitter
        range_splitter = self.range_splitter
        params = [
            f"{self.line!r}",
            f"{splitter=!r}" if splitter != SPLITTER else "",
            f"{range_splitter=!r}" if range_splitter != RANGE_SPLITTER else "",
        ]
        params_ = ", ".join([s for s in params if s])
        return f"{self.__class__.__name__}({params_})"

    def __hash__(self) -> int:
        return self.line.__hash__()

    def __eq__(self, other) -> bool:
        """== equality"""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """< less than"""
        if self.__class__ == other.__class__:
            return self.line < other.line
        return False

    # ============================= init =============================

    @property
    def line(self) -> str:
        """Ranges in <str> format"""
        return self._line

    @line.setter
    def line(self, line: str) -> None:
        if not isinstance(line, str):
            raise TypeError(f"{line=} {str} expected")
        line_: str = self._valid_line(line)
        line_ = line_.replace(self.range_splitter, RANGE_SPLITTER)
        line_ = line_.replace(self.splitter, SPLITTER)
        items = line_.split(SPLITTER)
        items = [s for s in items if s]
        ranges: LRange = sorted([Range(s) for s in set(items)])
        ports: SInt = {i for o in ranges for i in o.range}
        self._ports = sorted(ports)
        self._line = self._sports(ports)

    @property
    def ports(self) -> LInt:
        """Ranges in ist of <int> format"""
        return self._ports

    # =========================== helpers ============================

    def _valid_line(self, line: str) -> str:
        """Check valid chars in line. Split line to items by self.splitter"""
        lines: LStr = []
        splitter = self.splitter
        range_splitter = self.range_splitter
        lines_ = line.split(range_splitter)
        for line_ in lines_:
            items_: LStr = line_.split(splitter)
            items_ = [s for s in items_ if s]
            for item in items_:
                if not item.isdigit():
                    raise ValueError(f"invalid {item=} in {line=}, expected {splitter=}")
            line_ = splitter.join(items_)
            lines.append(line_)
        return range_splitter.join(lines)

    def _sports(self, items: IInt) -> str:
        """Convert list of <int> to <str>.
        :param items: [1, 3, 4, 5]
        :return: "1,3-5"
        """
        ranges: LStr = []  # return
        range_splitter = self.range_splitter
        item_1st: OInt = None
        items_: LInt = sorted({int(i) for i in items})
        for idx, item in enumerate(items_, start=1):
            # not last iteration
            if idx < len(items_):
                item_next = items_[idx]
                if item_next - item <= 1:  # range
                    if item_1st is None:  # start new range
                        item_1st = item
                else:  # int or end of range
                    if item_1st is None:
                        range_ = str(item)
                    else:
                        range_ = f"{item_1st}{range_splitter}{item}"
                    ranges.append(range_)
                    item_1st = None
            # last iteration
            else:
                item_ = str(item) if item_1st is None else f"{item_1st}{range_splitter}{item}"
                ranges.append(item_)
        return self.splitter.join(ranges)


# ============================= helpers ==============================

def check_tcp_range(ports: LInt) -> bool:
    """True if all ports are in the valid TCP/UDP range 1...65535, else raise ERROR."""
    if invalid_vlans := [i for i in ports if i < 1 or i > 65535]:
        raise ValueError(f"{invalid_vlans=}, expected in range 1...65535")
    return True


def check_vlans_range(vlans: LInt) -> bool:
    """True if all vlans are in the valid range 1...4094, else raise ERROR."""
    if invalid_vlans := [i for i in vlans if i < 1 or i > 4094]:
        raise ValueError(f"{invalid_vlans=}, expected in range 1...4094")
    return True
