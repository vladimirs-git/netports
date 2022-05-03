"""Ranges"""

from functools import total_ordering

from netports.range import Range, LRange
from netports.static import SPLITTER, RANGE_SPLITTER
from netports.types_ import LStr, LInt, OInt, SInt, IInt


@total_ordering
class Ranges:
    """Ranges"""

    __slots__ = ("_line", "_numbers", "splitter", "range_splitter", "_valid_chars", "_strict")

    def __init__(self, line: str, **kwargs):
        """Ranges.
        :param line: Range in <str> format.
        :param splitter: Separator character between numbers. By default ",".
        :param range_splitter: Separator between min and max digits in range. By default "-".
        :param strict: True - Raise ValueError, if in line is invalid item.
                       False - Make Range without invalid items. By default True.
        """
        self.splitter = kwargs.get("splitter") or SPLITTER
        self.range_splitter = kwargs.get("range_splitter") or RANGE_SPLITTER
        self._strict = self._init_strict(**kwargs)
        self._numbers: LInt = []
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

    @staticmethod
    def _init_strict(**kwargs) -> bool:
        """Init strict"""
        strict = kwargs.get("strict")
        if strict is None:
            return True
        if isinstance(strict, bool):
            return strict
        raise TypeError(f"{strict=} {bool} expected")

    # =========================== property ===========================

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
        items: LStr = line_.split(SPLITTER)
        items = [s for s in items if s]
        ranges = self._ranges(items)
        numbers: SInt = {i for o in ranges for i in o.range}
        self._numbers = sorted(numbers)
        self._line = self._snumbers(numbers)

    @property
    def numbers(self) -> LInt:
        """Ranges in ist of <int> format"""
        return self._numbers

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
                    if not self._strict:
                        continue
                    raise ValueError(f"invalid {item=} in {line=}")
            line_ = splitter.join(items_)
            lines.append(line_)
        return range_splitter.join(lines)

    def _snumbers(self, items: IInt) -> str:
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

    def _ranges(self, items: LStr) -> LRange:
        """Convert items to list of Range.
        If self._strict==True, raise ValueError, else skip invalid item."""
        ranges: LRange = []
        for item in items:
            try:
                ranges.append(Range(item))
            except ValueError as ex:
                if self._strict:
                    raise type(ex)(*ex.args)
                continue
        return ranges
