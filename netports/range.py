"""**Range** - An object that converts items to *object*
that represents range as *str* and as *List[int]*."""

from __future__ import annotations

from functools import total_ordering

from netports import helpers as h
from netports.item import Item, LItem
from netports.static import SPLITTER, RANGE_SPLITTER
from netports.types_ import LStr, LInt, OInt, IInt, T2SInt, StrInt, StrIInt, IStrInt


@total_ordering
class Range:
    """**Range** - An object that converts items to *object*
    that represents range as *str* and as *List[int]*"""

    def __init__(self, items: StrIInt = "", **kwargs):
        """Range
        :param items: Range of numbers. Numbers can be unsorted and duplicated.
            Type: *str*, *List[int]*.
        :param splitter: Separator character between numbers, by default ","
        :param range_splitter: Separator between min and max digits in range, by default "-"
        :param strict: True - Raise ValueError, if in line is invalid item.
                       False - Make Range without invalid items, By default - True.
        """
        self.splitter = kwargs.get("splitter") or SPLITTER
        self.range_splitter = kwargs.get("range_splitter") or RANGE_SPLITTER
        self._strict = self._init_strict(**kwargs)
        self._items: LItem = []
        self._idx = 0

        if isinstance(items, str):
            self.line = items
        elif isinstance(items, int):
            self._items = self._create_items([items])
        elif isinstance(items, (list, set, tuple)):
            self._items = self._create_items(items)
        else:
            raise TypeError(f"{items=} {str} expected")

    # ======================= special methods ========================

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
        return tuple(self._items).__hash__()

    def __eq__(self, other) -> bool:
        """== Equality"""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other: Range) -> bool:
        """< Less than"""
        if self.__class__ == other.__class__:
            self_len = len(self._items)
            other_len = len(other._items)
            if not (self_len and other_len):
                return self_len < other_len
            for idx, self_item in enumerate(self._items):
                try:
                    other_item = other._items[idx]
                except IndexError:
                    return False
                if self_item.min != other_item.min:
                    return self_item.min < other_item.min
                if self_item.max != other_item.max:
                    return self_item.max < other_item.max
            return self.line < other.line
        return False

    def __add__(self, other: Range) -> Range:
        """+ Add"""
        self_numbers, other_numbers = self._numbers_sets(other)
        self_numbers.update(other_numbers)
        return Range(self_numbers)

    def __sub__(self, other: Range) -> Range:
        """- Subtract"""
        self_numbers, other_numbers = self._numbers_sets(other)
        self_numbers.difference_update(other_numbers)
        return Range(self_numbers)

    def __contains__(self, number: int) -> bool:
        """Returns key in self"""
        if not isinstance(number, int):
            raise TypeError
        return number in self.numbers()

    def __delitem__(self, idx: int) -> None:
        """Deletes self.numbers[idx]"""
        numbers = self.numbers()
        numbers.__delitem__(idx)
        self._items = self._create_items(numbers)

    def __getitem__(self, idx: int):
        """Returns number by index"""
        return self.numbers()[idx]

    def __iter__(self):
        """Iterator"""
        return self

    def __len__(self) -> int:
        """Returns length of numbers"""
        return len(self.numbers())

    def __next__(self) -> int:
        """Returns next number"""
        try:
            number = self.numbers()[self._idx]
        except IndexError:
            raise StopIteration()
        self._idx += 1
        return number

    # ======================= list/set methods =======================

    def add(self, other: Range) -> None:
        """Adds other *Range* object to self"""
        self_numbers, other_numbers = self._numbers_sets(other)
        self_numbers.update(other_numbers)
        self._items = self._create_items(self_numbers)

    def append(self, number: StrInt) -> None:
        """Appends number to self"""
        number_ = h.to_int(number)
        other = Range(number_)
        self.add(other)

    def clear(self) -> None:
        """Removes all numbers from self"""
        self._items = []

    def copy(self):
        """Returns a copy of self *Range* object"""
        return Range(items=self.line,
                     splitter=self.splitter,
                     range_splitter=self.range_splitter,
                     strict=self._strict)

    def difference(self, other: Range) -> Range:
        """Returns the *Range* object of the difference between self and other *Range*"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.difference(other_numbers)
        return Range(numbers)

    def difference_update(self, other: Range) -> None:
        """Removes other *Range* from self"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.difference(other_numbers)
        self._items = self._create_items(numbers)

    def discard(self, number: StrInt) -> None:
        """Removes the specified number from self *Range*"""
        number_ = h.to_int(number)
        numbers = set(self.numbers()).difference({number_})
        self._items = self._create_items(numbers)

    def extend(self, numbers: IInt) -> None:
        """Adds *List[int]* numbers to self"""
        if not isinstance(numbers, (list, set, tuple)):
            raise TypeError(f"{numbers=} {list} expected")
        other = Range(numbers)
        self.add(other)

    def index(self, number: StrInt) -> int:
        """Index of number
        :return: Returns index of number
        :raises ValueError: if the number is not present in range
        """
        number_ = h.to_int(number)
        return self.numbers().index(number_)

    def intersection(self, other: Range) -> Range:
        """Returns *Range* which is the intersection of self and other *Range*"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.intersection(other_numbers)
        return Range(numbers)

    def intersection_update(self, other: Range) -> None:
        """Removes numbers of other *Range* in self, that are not present in other"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.intersection(other_numbers)
        self._items = self._create_items(numbers)

    def isdisjoint(self, other: Range) -> bool:
        """Returns whether self numbers and other *Range* numbers have intersection or not"""
        self_numbers, other_numbers = self._numbers_sets(other)
        return self_numbers.isdisjoint(other_numbers)

    def issubset(self, other: Range) -> bool:
        """Returns whether other *Range* numbers contains self numbers or not"""
        self_numbers, other_numbers = self._numbers_sets(other)
        return self_numbers.issubset(other_numbers)

    def issuperset(self, other: Range) -> bool:
        """Returns whether self *Range* numbers contains other *Range* numbers set or not"""
        self_numbers, other_numbers = self._numbers_sets(other)
        return self_numbers.issuperset(other_numbers)

    def pop(self) -> int:
        """Removes and returns last number in *Range*
        :raises IndexError: If list is empty or index is out of range
        """
        numbers = self.numbers()
        number = numbers.pop()
        self._items = self._create_items(numbers)
        return number

    def remove(self, number: StrInt) -> None:
        """Removes the specified number from self *Range*
        :raises ValueError: If the numbers is not present
        """
        number_ = h.to_int(number)
        numbers = self.numbers()
        numbers.remove(number_)
        self._items = self._create_items(numbers)

    def symmetric_difference(self, other: Range) -> Range:
        """Returns *Range* object with the symmetric differences of self and other *Range*"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.symmetric_difference(other_numbers)
        return Range(numbers)

    def symmetric_difference_update(self, other: Range) -> None:
        """Inserts the symmetric differences from self *Range* and other *Range*"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.symmetric_difference(other_numbers)
        self._items = self._create_items(numbers)

    def union(self, other: Range) -> Range:
        """Returns Range of the union of self and other numbers"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.union(other_numbers)
        return Range(numbers)

    def update(self, other: Range) -> None:
        """Returns *Range* of the union of self *Range* and other *Range*"""
        self_numbers, other_numbers = self._numbers_sets(other)
        numbers = self_numbers.union(other_numbers)
        self._items = self._create_items(numbers)

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
        """Range in *str* format"""
        return self._items_to_line(self._items)

    @line.setter
    def line(self, line: str) -> None:
        if not isinstance(line, str):
            raise TypeError(f"{line=} {str} expected")
        line_: str = self._valid_line(line)
        line_ = line_.replace(self.range_splitter, RANGE_SPLITTER)
        line_ = line_.replace(self.splitter, SPLITTER)
        lines: LStr = line_.split(SPLITTER)
        items = self._create_items(lines)
        self._items = items

    # =========================== methods ============================

    def numbers(self) -> LInt:
        """Returns list of numbers"""
        return [i for o in self._items for i in o.range]

    # =========================== helpers ============================

    def _items_to_line(self, items: LItem) -> str:
        """Converts  items *List[Item]* to line *str*
        :param items: [Item("1"), Item("3-5")]
        :return: "1,3-5"
        """
        lines = [o.line.replace("-", self.range_splitter) for o in items]
        line = self.splitter.join(lines)
        return line

    @staticmethod
    def _items_wo_duplicates(items: LItem) -> LItem:
        """Removes duplicates digits in items
        :param items: [Item(1), Item(4-5), Item(3-4), Item(1)]
        :return: [Item(1), Item(3-5)]
        """
        items_: LStr = []  # result
        numbers: LInt = sorted({i for o in items for i in o.range})
        item_1st: OInt = None
        for idx, item in enumerate(numbers, start=1):
            # not last iteration
            if idx < len(numbers):
                item_next = numbers[idx]
                if item_next - item <= 1:  # range
                    if item_1st is None:  # start new range
                        item_1st = item
                else:  # int or end of range
                    if item_1st is None:
                        range_ = str(item)
                    else:
                        range_ = f"{item_1st}-{item}"
                    items_.append(range_)
                    item_1st = None
            # last iteration
            else:
                item_ = str(item) if item_1st is None else f"{item_1st}-{item}"
                items_.append(item_)
        return [Item(s) for s in items_]

    def _numbers_sets(self, other: Range) -> T2SInt:
        """Converts self and other *List[int]* numbers to *Set[int]*
        :param other: Other Range *object*
        :return: Sets of numbers
        """
        if not isinstance(other, Range):
            raise TypeError(f"{other=} {Range} expected")
        self_numbers = self.numbers()
        other_numbers = other.numbers()
        return set(self_numbers), set(other_numbers)

    def _create_items(self, items: IStrInt) -> LItem:
        """Converts items *List[str]* to items *List[Items]*, removes duplicates
        :param items: List of *str* items
        :return: List of *Item* objects
        :raises ValueError: If self._strict==True and item is invalid
        """
        items_: LItem = []
        items_wo_duplicates = sorted(set([str(i) for i in items]))
        for item in items_wo_duplicates:
            if item == "":
                continue
            try:
                items_.append(Item(str(item)))
            except ValueError as ex:
                if self._strict:
                    raise type(ex)(*ex.args)
                continue
        items_ = self._items_wo_duplicates(items_)
        return items_

    def _valid_line(self, line: str) -> str:
        """Checks valid chars in line. Splits line to items by splitter"""
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
