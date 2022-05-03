"""unittest ranges.py"""

import unittest

from netports import Ranges
from tests.helpers_test import Helpers


class Test(Helpers):
    """Ranges"""

    def test_valid__line(self):
        """Ranges.line"""
        for kwargs, req_d in [
            (dict(line=""), dict(line="", numbers=[])),
            (dict(line="0"), dict(line="0", numbers=[0])),
            (dict(line="0,1"), dict(line="0-1", numbers=[0, 1])),
            (dict(line="0,2"), dict(line="0,2", numbers=[0, 2])),
            (dict(line="0 1", splitter=" "), dict(line="0-1", numbers=[0, 1])),
            (dict(line="0 2", splitter=" "), dict(line="0 2", numbers=[0, 2])),
            (dict(line="0-1"), dict(line="0-1", numbers=[0, 1])),
            (dict(line="0 to 1", range_splitter=" to "), dict(line="0 to 1", numbers=[0, 1])),
            (dict(line="1,3-5"), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(line="1,3,4,5,3-4,4-5,3-5"), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
            (dict(line="1 3 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5", numbers=[1, 3, 4, 5])),
            (dict(line="1 3 to 5 7 9 to 10 1 4 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5 7 9 to 10", numbers=[1, 3, 4, 5, 7, 9, 10])),
            (dict(line="1,3-5,a,7-a,a-7", strict=False), dict(line="1,3-5", numbers=[1, 3, 4, 5])),
        ]:
            # getter
            ranges_o = Ranges(**kwargs)
            self._test_attrs(obj=ranges_o, req_d=req_d, msg=f"getter {kwargs=}")
            # setter
            ranges_o.line = kwargs["line"]
            self._test_attrs(obj=ranges_o, req_d=req_d, msg=f"setter {kwargs=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del ranges_o.line

    def test_invalid__line(self):
        """Range.line"""
        for kwargs, error in [
            (dict(line=1), TypeError),
            (dict(line=["1"]), TypeError),
            (dict(line="0.1"), ValueError),  # invalid char
            (dict(line="0,1", splitter=" "), ValueError),  # invalid splitter
            (dict(line="0-1", range_splitter=" to "), ValueError),  # # invalid range_splitter
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                Ranges(**kwargs)

    # =========================== helpers ============================

    def test_valid__ranges(self):
        """Ranges._ranges()"""
        for items, strict, req in [
            ([], True, []),
            ([], False, []),
            (["1", "3-5"], True, ["1", "3-5"]),
            (["1", "3-5"], False, ["1", "3-5"]),
            (["3-"], False, []),
            (["-5"], False, []),
            (["1-3-5"], False, []),
            (["a"], False, []),
            (["3-a"], False, []),
            (["a-3"], False, []),
            (["1", "3-5", "a"], False, ["1", "3-5"]),
        ]:
            ranges_o = Ranges("1", strict=strict)
            result_l = ranges_o._ranges(items=items)
            result = [o.line for o in result_l]
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__ranges(self):
        """Ranges._ranges()"""
        for items, error in [
            (["a"], ValueError),
        ]:
            ranges_o = Ranges("1", strict=True)
            with self.assertRaises(error, msg=f"{items=}"):
                ranges_o._ranges(items=items)


if __name__ == "__main__":
    unittest.main()
