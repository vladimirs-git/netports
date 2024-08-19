"""Tests range.py"""

import unittest

from netports import Range, Item, NetportsValueError
from tests.helpers_ import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """Range"""

    # ======================= special methods ========================

    def test_valid__hash__(self):
        """Range.__hash__()"""
        range_o = Range("1,3-5")
        result = hash(range_o)
        req = hash((Item("1"), Item("3-5")))
        self.assertEqual(result, req, msg="hash")

    def test_valid__eq__(self):
        """Range.__eq__() __ne__()"""
        line = "1,3-5"
        range_o = Range(line)
        for other_o, req, in [
            (Range(line), True),
            (Range("1,3,4,5"), True),
            (Range("1"), False),
        ]:
            result = range_o == other_o
            self.assertEqual(result, req, msg=f"{range_o=} {other_o=}")
            result = range_o != other_o
            self.assertEqual(result, not req, msg=f"{range_o=} {other_o=}")

    def test_valid__lt__(self):
        """Range.__lt__() __le__() __gt__() __ge__()"""
        for range_o, other_o, req_lt, req_le, req_gt, req_ge in [
            (Range("0"), "0", False, False, True, True),
            (Range(), Range(), False, True, False, True),
            (Range(), Range("0"), True, True, False, False),
            (Range("0"), Range(), False, False, True, True),
            (Range("0"), Range("0"), False, True, False, True),
            (Range("0"), Range("1"), True, True, False, False),
            (Range("1"), Range("0"), False, False, True, True),
            (Range("1"), Range("1"), False, True, False, True),
            (Range("1,3-5"), Range("0"), False, False, True, True),
            (Range("1,3-5"), Range("1"), False, False, True, True),
            (Range("1,3-5"), Range("2"), True, True, False, False),
            (Range("1,3-5"), Range("6"), True, True, False, False),
            (Range("1,3-5"), Range("3-5"), True, True, False, False),
            (Range("1,3-5"), Range("1,3-5"), False, True, False, True),
        ]:
            result = range_o < other_o
            self.assertEqual(result, req_lt, msg=f"{range_o=} {other_o=}")
            result = range_o <= other_o
            self.assertEqual(result, req_le, msg=f"{range_o=} {other_o=}")
            result = range_o > other_o
            self.assertEqual(result, req_gt, msg=f"{range_o=} {other_o=}")
            result = range_o >= other_o
            self.assertEqual(result, req_ge, msg=f"{range_o=} {other_o=}")

    def test_valid__lt__sort(self):
        """Range.__lt__(), Range.__le__()"""
        range_o = "1,3-5"
        for items in [
            [Range("0"), Range(range_o)],
            [Range("0-6"), Range(range_o)],
            [Range("1"), Range(range_o)],
            [Range(range_o), Range("2")],
            [Range(range_o), Range("6")],
            [Range(range_o), Range("3-5")],
            [Range(range_o), Range(range_o)],
        ]:
            req = items.copy()
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__add__(self):
        """Range.__add__()"""
        line1 = "1,3-5"
        range1 = Range(line1)
        for line2, req, in [
            ("0", "0-1,3-5"),
            ("1", "1,3-5"),
            ("2", "1-5"),
            ("3", "1,3-5"),
            ("4", "1,3-5"),
            ("5", "1,3-5"),
            ("6", "1,3-6"),
            ("7", "1,3-5,7"),
        ]:
            range2 = Range(line2)
            range3 = range1 + range2
            result = range1.line
            self.assertEqual(result, line1, msg=f"{range1=} {line2=}")
            result = range2.line
            self.assertEqual(result, line2, msg=f"{range1=} {line2=}")
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line2=}")

    def test_valid__sub__(self):
        """Range.__sub__()"""
        line1 = "1,3-5"
        range1 = Range(line1)
        for line2, req, in [
            ("0", "1,3-5"),
            ("1", "3-5"),
            ("2", "1,3-5"),
            ("3", "1,4-5"),
            ("4", "1,3,5"),
            ("5", "1,3-4"),
            ("6", "1,3-5"),
            ("7", "1,3-5"),
        ]:
            range2 = Range(line2)
            range3 = range1 - range2
            result = range1.line
            self.assertEqual(result, line1, msg=f"{range1=} {line2=}")
            result = range2.line
            self.assertEqual(result, line2, msg=f"{range1=} {line2=}")
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line2=}")

    def test_valid__contains__(self):
        """Range.__contains__()"""
        range_o = Range("1,3-5")
        for number, req, in [
            (0, False),
            (1, True),
            (2, False),
            (3, True),
            (4, True),
            (5, True),
            (6, False),
        ]:
            result = number in range_o
            self.assertEqual(result, req, msg=f"{number=}")

    def test_valid__delitem__(self):
        """Range.__delitem__()"""
        for idx, req, in [
            (0, "3-5"),
            (1, "1,4-5"),
            (2, "1,3,5"),
            (3, "1,3-4"),
            (-1, "1,3-4"),
        ]:
            range_o = Range("1,3-5")
            del range_o[idx]
            result = range_o.line
            self.assertEqual(result, req, msg=f"{idx=}")

    def test_invalid__delitem__(self):
        """Range.__delitem__()"""
        for idx, error, in [
            (4, IndexError),
        ]:
            range_o = Range("1,3-5")
            with self.assertRaises(error, msg=f"{idx=}"):
                del range_o[idx]

    def test_valid__getitem__(self):
        """Range.__getitem__()"""
        range_o = Range("1,3-5")
        for idx, req, in [
            (0, 1),
            (1, 3),
            (2, 4),
            (3, 5),
            (-1, 5),
        ]:
            result = range_o[idx]
            self.assertEqual(result, req, msg=f"{idx=}")

    def test_invalid__getitem__(self):
        """Range.__getitem__()"""
        for idx, error, in [
            (4, IndexError),
        ]:
            range_o = Range("1,3-5")
            with self.assertRaises(error, msg=f"{idx=}"):
                _ = range_o[idx]

    def test_valid__iter__(self):
        """Range.__iter__()"""
        range_o = Range("1,3-5")
        for result in range_o:
            _ = result

    def test_valid__len__(self):
        """Range.__len__()"""
        for line, req, in [
            ("1", 1),
            ("1,3", 2),
            ("3-5", 3),
            ("1,3-5", 4),
        ]:
            range_o = Range(line)
            result = len(range_o)
            self.assertEqual(result, req, msg=f"{line=}")

    def test_valid__next__(self):
        """Range.__next__()"""
        range_o = Range("1,3-5")
        for req in [
            1,
            3,
            4,
            5,
        ]:
            result = next(range_o)
            self.assertEqual(result, req, msg=f"{req=}")

    # ======================= list/set methods =======================

    def test_valid__add(self):
        """Range.add()"""
        for line, req, in [
            ("0", "0-1,3-5"),
            ("1", "1,3-5"),
            ("2", "1-5"),
            ("3", "1,3-5"),
            ("4", "1,3-5"),
            ("5", "1,3-5"),
            ("6", "1,3-6"),
            ("7", "1,3-5,7"),
        ]:
            range1 = Range("1,3-5")
            range2 = Range(line)
            range1.add(range2)
            result = range1.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__append(self):
        """Range.append()"""
        for number, req, in [
            (3, "1,3"),
            ("3", "1,3"),
        ]:
            range_o = Range("1")
            range_o.append(number)
            result = range_o.line
            self.assertEqual(result, req, msg=f"{range_o=} {number=}")

    def test_invalid__append(self):
        """Range.append()"""
        range_o = Range()
        for number, error, in [
            ([3], TypeError),
            (["3"], TypeError),
        ]:
            with self.assertRaises(error, msg=f"{number=}"):
                range_o.append(number)

    def test_valid__clear(self):
        """Range.clear()"""
        range_o = Range("1")
        range_o.clear()
        result = range_o.line
        self.assertEqual(result, "", msg="clear")
        result = range_o.numbers()
        self.assertEqual(result, [], msg="clear")

    def test_valid__copy(self):
        """Range.copy()"""
        range1 = Range("1")
        range2 = range1.copy()
        range2.append("2")
        result = range1.line
        self.assertEqual(result, "1", msg="copy")
        result = range2.line
        self.assertEqual(result, "1-2", msg="copy")

    def test_valid__difference(self):
        """Range.difference()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0", "1,3-5"),
            ("1", "3-5"),
            ("2", "1,3-5"),
            ("3", "1,4-5"),
            ("4", "1,3,5"),
            ("5", "1,3-4"),
            ("6", "1,3-5"),
        ]:
            range2 = Range(line)
            range3 = range1.difference(range2)
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range1.line
            self.assertEqual(result, "1,3-5", msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__difference_update(self):
        """Range.difference_update()"""
        for line, req, in [
            ("0", "1,3-5"),
            ("1", "3-5"),
            ("2", "1,3-5"),
            ("3", "1,4-5"),
            ("4", "1,3,5"),
            ("5", "1,3-4"),
            ("6", "1,3-5"),
        ]:
            range1 = Range("1,3-5")
            range2 = Range(line)
            range1.difference_update(range2)
            result = range1.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__discard(self):
        """Range.discard()"""
        for number, req, in [
            ("1", "3-5"),
            (2, "1,3-5"),
            (3, "1,4-5"),
        ]:
            range_o = Range("1,3-5")
            range_o.discard(number)
            result = range_o.line
            self.assertEqual(result, req, msg=f"{range_o=} {number=}")

    def test_valid__extend(self):
        """Range.extend()"""
        for numbers, req, in [
            ([3], "1,3"),
            ([3], "1,3"),
            (["3"], "1,3"),
            ([3, 4, 5], "1,3-5"),
        ]:
            range_o = Range("1")
            range_o.extend(numbers)
            result = range_o.line
            self.assertEqual(result, req, msg=f"{numbers=}")

    def test_invalid__extend(self):
        """Range.extend()"""
        range_o = Range()
        for number, error, in [
            (3, TypeError),
            ("3", TypeError),
            (["a"], NetportsValueError),
        ]:
            with self.assertRaises(error, msg=f"{number=}"):
                range_o.extend(number)

    def test_valid__index(self):
        """Range.index()"""
        range_o = Range("1,3-5")
        for item, req in [
            (1, 0),
            ("3", 1),
            (4, 2),
            (5, 3),
        ]:
            result = range_o.index(item)
            self.assertEqual(result, req, msg=f"{item=}")

    def test_invalid__index(self):
        """Range.index()"""
        range_o = Range("1,3-5")
        for item, error in [
            (2, ValueError),
        ]:
            with self.assertRaises(error, msg=f"{item=}"):
                range_o.index(item)

    def test_valid__intersection(self):
        """Range.intersection()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", ""),
            ("0-3", "1,3"),
            ("5-7", "5"),
        ]:
            range2 = Range(line)
            range3 = range1.intersection(range2)
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range1.line
            self.assertEqual(result, "1,3-5", msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__intersection_update(self):
        """Range.intersection_update()"""
        for line, req, in [
            ("0,6", ""),
            ("0-3", "1,3"),
            ("5-7", "5"),
        ]:
            range1 = Range("1,3-5")
            range2 = Range(line)
            range1.intersection_update(range2)
            result = range1.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__isdisjoint(self):
        """Range.isdisjoint()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", True),
            ("1", False),
            ("5-7", False),
        ]:
            range2 = Range(line)
            result = range1.isdisjoint(range2)
            self.assertEqual(result, req, msg=f"{range1=} {line=}")

    def test_valid__issubset(self):
        """Range.issubset()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", False),
            ("1", False),
            ("5-7", False),
            ("1,3-5", True),
            ("1-5", True),
        ]:
            range2 = Range(line)
            result = range1.issubset(range2)
            self.assertEqual(result, req, msg=f"{range1=} {line=}")

    def test_valid__issuperset(self):
        """Range.issuperset()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", False),
            ("1", True),
            ("5-7", False),
            ("1,3-5", True),
            ("1-5", False),
        ]:
            range2 = Range(line)
            result = range1.issuperset(range2)
            self.assertEqual(result, req, msg=f"{range1=} {line=}")

    def test_valid__pop(self):
        """Range.pop()"""
        range_o = Range("1,3-5")
        for number, req in [
            (5, "1,3-4"),
            (4, "1,3"),
        ]:
            result_ = range_o.pop()
            self.assertEqual(result_, number, msg=f"{number=}")
            result = range_o.line
            self.assertEqual(result, req, msg=f"{number=}")

    def test_invalid__pop(self):
        """Range.pop()"""
        range_o = Range()
        for error in [
            IndexError
        ]:
            with self.assertRaises(error, msg="pop"):
                range_o.pop()

    def test_valid__remove(self):
        """Range.remove()"""
        range_o = Range("1,3-5")
        for number, req in [
            (4, "1,3,5"),
            ("3", "1,5"),
        ]:
            range_o.remove(number)
            result = range_o.line
            self.assertEqual(result, req, msg=f"{number=}")

    def test_invalid__remove(self):
        """Range.remove()"""
        range_o = Range("1,3-5")
        for number, error in [
            (6, ValueError),
        ]:
            with self.assertRaises(error, msg=f"{number=}"):
                range_o.remove(number)

    def test_valid__symmetric_difference(self):
        """Range.symmetric_difference()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", "0-1,3-6"),
            ("1", "3-5"),
            ("2", "1-5"),
            ("1,3-5", ""),
        ]:
            range2 = Range(line)
            range3 = range1.symmetric_difference(range2)
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range1.line
            self.assertEqual(result, "1,3-5", msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__symmetric_difference_update(self):
        """Range.symmetric_difference_update()"""
        for line, req, in [
            ("0,6", "0-1,3-6"),
            ("1", "3-5"),
            ("2", "1-5"),
            ("1,3-5", ""),
        ]:
            range1 = Range("1,3-5")
            range2 = Range(line)
            range1.symmetric_difference_update(range2)
            result = range1.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__union(self):
        """Range.union()"""
        range1 = Range("1,3-5")
        for line, req, in [
            ("0,6", "0-1,3-6"),
            ("1", "1,3-5"),
            ("2", "1-5"),
            ("1,3-5", "1,3-5"),
        ]:
            range2 = Range(line)
            range3 = range1.union(range2)
            result = range3.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range1.line
            self.assertEqual(result, "1,3-5", msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_valid__update(self):
        """Range.update()"""
        for line, req, in [
            ("0,6", "0-1,3-6"),
            ("1", "1,3-5"),
            ("2", "1-5"),
            ("1,3-5", "1,3-5"),
        ]:
            range1 = Range("1,3-5")
            range2 = Range(line)
            range1.update(range2)
            result = range1.line
            self.assertEqual(result, req, msg=f"{range1=} {line=}")
            result = range2.line
            self.assertEqual(result, line, msg=f"{range1=} {line=}")

    def test_invalid__methods(self):
        """Range.__add__()
        Range.__sub__()
        Range.add()
        Range.difference()
        Range.symmetric_difference()
        Range.isdisjoint()
        Range.issubset()
        Range.issuperset()
        Range.difference_update()
        Range.symmetric_difference_update()
        Range.union()
        Range.update()
        """
        for line, error, in [
            ("1", TypeError),
            (1, TypeError),
        ]:
            range_o = Range("0")
            with self.assertRaises(error, msg=f"{line=}"):
                _ = range_o + line
            with self.assertRaises(error, msg=f"{line=}"):
                _ = range_o - line
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.add(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.difference(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.difference_update(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.isdisjoint(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.issubset(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.issuperset(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.symmetric_difference(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.symmetric_difference_update(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.union(line)
            with self.assertRaises(error, msg=f"{line=}"):
                range_o.update(line)

    # =========================== property ===========================

    def test_valid__line(self):
        """Range.line"""
        for kwargs, req_d in [
            # line
            ({}, dict(line="", numbers=[])),
            (dict(items=""), dict(line="", numbers=[])),
            (dict(items="0"), dict(line="0", numbers=[0])),
            (dict(items="0,1"), dict(line="0-1", numbers=[0, 1])),
            (dict(items="0,2"), dict(line="0,2", numbers=[0, 2])),
            (dict(items="0 1", splitter=" "), dict(line="0-1", numbers=[0, 1])),
            (dict(items="0 2", splitter=" "), dict(line="0 2", numbers=[0, 2])),
            (dict(items="0-1"), dict(line="0-1", numbers=[0, 1])),
            (dict(items="0 to 1", range_splitter=" to "), dict(line="0 to 1", numbers=[0, 1])),
            (dict(items="1,3-5"), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(items="1,3,4,5,3-4,4-5,3-5"), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(items="1 3 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5", numbers=[1, 3, 4, 5])),
            (dict(items="1 3 to 5 7 9 to 10 1 4 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5 7 9 to 10", numbers=[1, 3, 4, 5, 7, 9, 10])),
            (dict(items="1,3-5,a,7-a,a-7", strict=False), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            # numbers
            (dict(items=0), dict(line="0", numbers=[0])),
            (dict(items=1), dict(line="1", numbers=[1])),
            (dict(items=[0]), dict(line="0", numbers=[0])),
            (dict(items=[0, 1]), dict(line="0-1", numbers=[0, 1])),
            (dict(items=["0", "1"]), dict(line="0-1", numbers=[0, 1])),
            (dict(items=[0, 2]), dict(line="0,2", numbers=[0, 2])),
            (dict(items={0, 2}), dict(line="0,2", numbers=[0, 2])),
            (dict(items=(0, 2)), dict(line="0,2", numbers=[0, 2])),
            (dict(items=[1, 3, 4, 5]), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(items=[5, 1, 1, 3, 4]), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(items=[1, 3, 4, 5], splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5", numbers=[1, 3, 4, 5])),
        ]:
            # getter
            range_o = Range(**kwargs)
            self._test_attrs(obj=range_o, exp_d=req_d, msg=f"getter {kwargs=}")
            # setter
            if kwargs and isinstance(kwargs["items"], str):
                range_o.line = kwargs["items"]
                self._test_attrs(obj=range_o, exp_d=req_d, msg=f"setter {kwargs=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del range_o.line

    def test_invalid__line(self):
        """Range.line"""
        for kwargs, error in [
            (dict(items=-1), ValueError),
            (dict(items={1: "A"}), TypeError),
            (dict(items="0.1"), ValueError),  # invalid char
            (dict(items="0,1", splitter=" "), ValueError),  # invalid splitter
            (dict(items="0-1", range_splitter=" to "), ValueError),  # invalid range_splitter
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                Range(**kwargs)

    # =========================== helpers ============================

    def test_valid__create_items(self):
        """Range._create_items()"""
        for items, strict, req in [
            ([], True, []),
            ([], False, []),
            ([""], True, []),
            ([""], False, []),
            (["1", "3-5"], True, ["1", "3-5"]),
            (["1", "3-5"], False, ["1", "3-5"]),
            (["1", "3-5", "1", "3-4", "4-5"], True, ["1", "3-5"]),
            (["1", "3-5", "1", "3-4", "4-5"], False, ["1", "3-5"]),
            (["3-"], False, []),
            (["-5"], False, []),
            (["1-3-5"], False, []),
            (["a"], False, []),
            (["3-a"], False, []),
            (["a-3"], False, []),
            (["1", "3-5", "a"], False, ["1", "3-5"]),
        ]:
            range_o = Range("1", strict=strict)
            result_l = range_o._create_items(items=items)
            result = [o.line for o in result_l]
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__create_items(self):
        """Range._create_items()"""
        for items, error in [
            (["a"], ValueError),
        ]:
            range_o = Range("1", strict=True)
            with self.assertRaises(error, msg=f"{items=}"):
                range_o._create_items(items=items)

    def test_valid__items_to_line(self):
        """Range._items_to_line()"""
        for items, kwargs, req in [
            ([], {}, ""),
            ([Item("1")], {}, "1"),
            ([Item("3-5")], {}, "3-5"),
            ([Item("1"), Item("3-5")], {}, "1,3-5"),
            ([Item("1"), Item("3-5")], dict(splitter=" ", range_splitter=" to "), "1 3 to 5"),
        ]:
            range_o = Range("1", **kwargs)
            result = range_o._items_to_line(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__items_wo_duplicates(self):
        """Range._items_wo_duplicates()"""
        range_o = Range("1")
        for items, req in [
            ([], []),
            ([Item("1")], [Item("1")]),
            ([Item("3-5")], [Item("3-5")]),
            ([Item("3-5"), Item("1")], [Item("1"), Item("3-5")]),
            ([Item("1"), Item("3-5"), Item("1"), Item("3-4")], [Item("1"), Item("3-5")]),
        ]:
            result = range_o._items_wo_duplicates(items=items)
            self.assertEqual(result, req, msg=f"{items=}")


if __name__ == "__main__":
    unittest.main()
