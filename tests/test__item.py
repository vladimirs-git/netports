"""unittest item.py"""

import unittest

from netports import Item, NetportsValueError
from tests.helpers_ import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """Item"""

    # ========================== redefined ===========================

    def test_valid__hash__(self):
        """Item.__hash__()"""
        line = "1-2"
        item_o = Item(line)
        result = item_o.__hash__()
        req = hash((1, 2))
        self.assertEqual(result, req, msg=f"{line=}")

    def test_valid__eq__(self):
        """Item.__eq__() __ne__()"""
        item1 = "1-2"
        item_o = Item(item1)
        for other_o, req, in [
            (Item(item1), True),
            (Item("0-2"), False),
            (Item("1"), False),
            (Item("2"), False),
        ]:
            result = item_o.__eq__(other_o)
            self.assertEqual(result, req, msg=f"{item_o=} {other_o=}")
            result = item_o.__ne__(other_o)
            self.assertEqual(result, not req, msg=f"{item_o=} {other_o=}")

    def test_valid__lt__(self):
        """Item.__lt__() __le__() __gt__() __ge__()"""
        item1 = "1-2"
        for item_o, other_o, req_lt, req_le, req_gt, req_ge in [
            (Item(item1), item1, False, False, True, True),
            (Item(item1), Item(item1), False, True, False, True),
            (Item(item1), Item("0"), False, False, True, True),
            (Item(item1), Item("1"), False, False, True, True),
            (Item(item1), Item("2"), True, True, False, False),
            (Item(item1), Item("0-3"), False, False, True, True),
            (Item(item1), Item("2-3"), True, True, False, False),
            (Item(item1), Item("1-1"), False, False, True, True),
            (Item(item1), Item("1-3"), True, True, False, False),
        ]:
            result = item_o.__lt__(other_o)
            self.assertEqual(result, req_lt, msg=f"{item_o=} {other_o=}")
            result = item_o.__le__(other_o)
            self.assertEqual(result, req_le, msg=f"{item_o=} {other_o=}")
            result = item_o.__gt__(other_o)
            self.assertEqual(result, req_gt, msg=f"{item_o=} {other_o=}")
            result = item_o.__ge__(other_o)
            self.assertEqual(result, req_ge, msg=f"{item_o=} {other_o=}")

    def test_valid__lt__sort(self):
        """Item.__lt__(), Item.__le__()"""
        item1 = "1-2"
        for items in [
            [Item(item1), Item(item1)],
            [Item("0"), Item(item1)],
            [Item("1"), Item(item1)],
            [Item(item1), Item("2")],
            [Item("0-1"), Item(item1)],
            [Item(item1), Item("2-3")],
            [Item("1-1"), Item(item1)],
            [Item(item1), Item("1-3")],
        ]:
            req = items.copy()
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")

    # =========================== property ===========================

    def test_valid__line(self):
        """Item.line"""
        for line, req_d in [
            ("0", dict(line="0", min=0, max=0, range=range(0, 1))),
            ("1", dict(line="1", min=1, max=1, range=range(1, 2))),
            ("0-1", dict(line="0-1", min=0, max=1, range=range(0, 2))),
        ]:
            # getter
            item_o = Item(line)
            self._test_attrs(obj=item_o, exp_d=req_d, msg=f"getter {line=}")
            # setter
            item_o.line = line
            self._test_attrs(obj=item_o, exp_d=req_d, msg=f"setter {line=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del item_o.line

    def test_invalid__line(self):
        """Item.line"""
        for line, error in [
            (1, TypeError),
            (["1"], TypeError),
            ("0,1", NetportsValueError),
            ("1,3-5", NetportsValueError),
        ]:
            with self.assertRaises(error, msg=f"{line=}"):
                Item(line)


if __name__ == "__main__":
    unittest.main()
