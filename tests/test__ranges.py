"""unittest ranges.py"""

import unittest

from netports import Ranges
from tests.helpers_test import Helpers


class Test(Helpers):
    """Ranges"""

    def test_valid__line(self):
        """Ranges.line"""
        for kwargs, req_d in [
            # (dict(line=""), dict(line="", ports=[])),
            # (dict(line="0"), dict(line="0", ports=[0])),
            # (dict(line="0,1"), dict(line="0-1", ports=[0, 1])),
            # (dict(line="0,2"), dict(line="0,2", ports=[0, 2])),
            # (dict(line="0 1", splitter=" "), dict(line="0-1", ports=[0, 1])),
            # (dict(line="0 2", splitter=" "), dict(line="0 2", ports=[0, 2])),
            # (dict(line="0-1"), dict(line="0-1", ports=[0, 1])),
            # (dict(line="0 to 1", range_splitter=" to "), dict(line="0 to 1", ports=[0, 1])),
            # (dict(line="1,3-5"), dict(line="1,3-5", ports=[1, 3, 4, 5])),
            # (dict(line="1,3,4,5,3-4,4-5,3-5"), dict(line="1,3-5", ports=[1, 3, 4, 5])),
            (dict(line="1 3 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5", ports=[1, 3, 4, 5])),
            (dict(line="1 3 to 5 7 9 to 10 1 4 to 5", splitter=" ", range_splitter=" to "),
             dict(line="1 3 to 5 7 9 to 10", ports=[1, 3, 4, 5, 7, 9, 10])),
        ]:
            # getter
            range_o = Ranges(**kwargs)
            self._test_attrs(obj=range_o, req_d=req_d, msg=f"getter {kwargs=}")
            # setter
            range_o.line = kwargs["line"]
            self._test_attrs(obj=range_o, req_d=req_d, msg=f"setter {kwargs=}")
        # deleter
        with self.assertRaises(AttributeError, msg="deleter line"):
            # noinspection PyPropertyAccess
            del range_o.line

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


if __name__ == "__main__":
    unittest.main()
