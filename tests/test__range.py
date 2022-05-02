"""unittest range.py"""

import unittest

from netports import Range
from tests.helpers_test import Helpers


# noinspection DuplicatedCode
class Test(Helpers):
    """Range"""

    # ========================== redefined ===========================

    def test_valid__hash__(self):
        """Range.__hash__()"""
        line = "1-2"
        range_o = Range(line)
        result = range_o.__hash__()
        req = hash((1, 2))
        self.assertEqual(result, req, msg=f"{line=}")

    def test_valid__eq__(self):
        """Range.__eq__() __ne__()"""
        range1 = "1-2"
        range_o = Range(range1)
        for other_o, req, in [
            (Range(range1), True),
            (Range("0-2"), False),
            (Range("1"), False),
            (Range("2"), False),
        ]:
            result = range_o.__eq__(other_o)
            self.assertEqual(result, req, msg=f"{range_o =} {other_o=}")
            result = range_o.__ne__(other_o)
            self.assertEqual(result, not req, msg=f"{range_o =} {other_o=}")

    def test_valid__lt__(self):
        """Range.__lt__() __le__() __gt__() __ge__()"""
        range1 = "1-2"
        for range_o, other_o, req_lt, req_le, req_gt, req_ge in [
            (Range(range1), range1, False, False, True, True),
            (Range(range1), Range(range1), False, True, False, True),
            (Range(range1), Range("0"), False, False, True, True),
            (Range(range1), Range("1"), False, False, True, True),
            (Range(range1), Range("2"), True, True, False, False),
            (Range(range1), Range("0-3"), False, False, True, True),
            (Range(range1), Range("2-3"), True, True, False, False),
            (Range(range1), Range("1-1"), False, False, True, True),
            (Range(range1), Range("1-3"), True, True, False, False),
        ]:
            result = range_o.__lt__(other_o)
            self.assertEqual(result, req_lt, msg=f"{range_o=} {other_o=}")
            result = range_o.__le__(other_o)
            self.assertEqual(result, req_le, msg=f"{range_o=} {other_o=}")
            result = range_o.__gt__(other_o)
            self.assertEqual(result, req_gt, msg=f"{range_o=} {other_o=}")
            result = range_o.__ge__(other_o)
            self.assertEqual(result, req_ge, msg=f"{range_o=} {other_o=}")

    def test_valid__lt__sort(self):
        """Ace.__lt__(), Ace.__le__()"""
        range1 = "1-2"
        for items in [
            [Range(range1), Range(range1)],
            [Range("0"), Range(range1)],
            [Range("1"), Range(range1)],
            [Range(range1), Range("2")],
            [Range("0-1"), Range(range1)],
            [Range(range1), Range("2-3")],
            [Range("1-1"), Range(range1)],
            [Range(range1), Range("1-3")],
        ]:
            req = items.copy()
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")
            items[0], items[1] = items[1], items[0]
            result = sorted(items)
            self.assertEqual(result, req, msg=f"{items=}")

    # =========================== property ===========================

    def test_valid__line(self):
        """Range.line"""
        for line, req_d in [
            ("0", dict(line="0", min=0, max=0, range=range(0, 1))),
            ("1", dict(line="1", min=1, max=1, range=range(1, 2))),
            ("0-1", dict(line="0-1", min=0, max=1, range=range(0, 2))),
        ]:
            # getter
            range_o = Range(line)
            self._test_attrs(obj=range_o, req_d=req_d, msg=f"getter {line=}")
            # setter
            range_o.line = line
            self._test_attrs(obj=range_o, req_d=req_d, msg=f"setter {line=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del range_o.line

    def test_invalid__line(self):
        """Range.line"""
        for line, error in [
            (1, TypeError),
            (["1"], TypeError),
            ("0,1", ValueError),
            ("1,3-5", ValueError),
        ]:
            with self.assertRaises(error, msg=f"{line=}"):
                Range(line)


if __name__ == "__main__":
    unittest.main()
