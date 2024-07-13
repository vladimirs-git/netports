"""Unittest sw_version.py"""

import unittest

from netports.swversion import SwVersion


class Test(unittest.TestCase):
    """SwVersion"""

    def _test_attrs(self, obj, req_d, msg: str):
        """Test obj.line and attributes in req_d
        :param obj: Tested object
        :param req_d: Valid attributes and values
        :param msg: Message
        """
        for attr, req in req_d.items():
            result = getattr(obj, attr)
            self.assertEqual(result, req, msg=f"{msg} {attr=}")

    def test_valid__hash__(self):
        """SwVersion.__hash__()"""
        for text, req in [
            # cisco_ios
            ("11.22(33)SE44", "11.22(33)se44"),
            ("11.22(33)se44", "11.22(33)se44"),
            # hp_procurve
            ("YA.11.22.0033", "ya.11.22.0033"),
            ("ya.11.22.0033", "ya.11.22.0033"),
        ]:
            obj = SwVersion(text)
            result = obj.__hash__()
            req_hash = req.lower().__hash__()
            self.assertEqual(result, req_hash, msg="__hash__")

    def test_valid__eq__(self):
        """SwVersion.__eq__() __ne__()"""

        for text1, text2, req in [
            # cisco_ios
            ("11.22(33)SE44", "11.22(33)SE44", True),
            ("1.22(33)SE44", "11.22(33)SE44", False),
            ("11.22(3)SE44", "11.22(33)SE44", False),
            ("11.22(33)SE4", "11.22(33)SE44", False),
            ("11.22(33)XX44", "11.22(33)SE44", False),
            ("11.22(33)", "11.22(33)SE44", False),
            # hp_procurve
            ("YA.11.22.0033", "YA.11.22.0033", True),
            ("YA.11.22.0033", "YA.11.22.0034", False),
            # combo
            ("11.22(33)", "YA.11.22.33", False),
        ]:
            obj1 = SwVersion(text1)
            obj2 = SwVersion(text2)
            result = obj2.__eq__(obj1)
            self.assertEqual(result, req, msg=f"{text1=}")

            req = not req
            result = obj2.__ne__(obj1)
            self.assertEqual(result, req, msg=f"{text1=}")

    def test_valid__lt__(self):
        """SwVersion.__lt__() __le__() __gt__() __ge__()"""
        v2_2_2b2 = "2.2(2)B2"
        v2_2_2a2 = "2.2(2)A2"
        v1_2_2a2 = "1.2(2)A2"
        v3_2_2a2 = "3.2(2)A2"
        v2_1_2a2 = "2.1(2)A2"
        v2_3_2a2 = "2.3(2)A2"
        v2_2_1a2 = "2.2(1)A2"
        v2_2_3a2 = "2.2(3)A2"
        v2_2_2a1 = "2.2(2)A1"
        v2_2_2a3 = "2.2(2)A3"
        for obj1, obj2, req_lt, req_le, req_gt, req_ge in [
            (SwVersion(v2_2_2a2), SwVersion(v2_2_2a2), False, True, False, True),
            (SwVersion(v2_2_2a2), SwVersion(v2_2_2b2), False, True, False, True),
            (SwVersion(v2_2_2a2), SwVersion(v1_2_2a2), False, False, True, True),
            (SwVersion(v2_2_2a2), SwVersion(v3_2_2a2), True, True, False, False),
            (SwVersion(v2_2_2a2), SwVersion(v2_1_2a2), False, False, True, True),
            (SwVersion(v2_2_2a2), SwVersion(v2_3_2a2), True, True, False, False),
            (SwVersion(v2_2_2a2), SwVersion(v2_2_1a2), False, False, True, True),
            (SwVersion(v2_2_2a2), SwVersion(v2_2_3a2), True, True, False, False),
            (SwVersion(v2_2_2a2), SwVersion(v2_2_2a1), False, False, True, True),
            (SwVersion(v2_2_2a2), SwVersion(v2_2_2a3), True, True, False, False),
        ]:
            result = obj1.__lt__(obj2)
            self.assertEqual(result, req_lt, msg=f"{obj1=} {obj2=}")
            result = obj1.__le__(obj2)
            self.assertEqual(result, req_le, msg=f"{obj1=} {obj2=}")
            result = obj1.__gt__(obj2)
            self.assertEqual(result, req_gt, msg=f"{obj1=} {obj2=}")
            result = obj1.__ge__(obj2)
            self.assertEqual(result, req_ge, msg=f"{obj1=} {obj2=}")

    def test_valid__lt__sort(self):
        """SwVersion.__lt__() __le__() __gt__() __ge__()"""
        unsorted = [
            "2.2(2)B2",
            "2.2(2)A2",
            "1.2(2)A2",
            "3.2(2)A2",
            "2.1(2)A2",
            "2.3(2)A2",
            "2.2(1)A2",
            "2.2(3)A2",
            "2.2(2)A1",
            "2.2(2)A3",
        ]
        req = [
            "1.2(2)a2",
            "2.1(2)a2",
            "2.2(1)a2",
            "2.2(2)a1",
            "2.2(2)b2",
            "2.2(2)a2",
            "2.2(2)a3",
            "2.2(3)a2",
            "2.3(2)a2",
            "3.2(2)a2",
        ]
        objs = [SwVersion(s) for s in unsorted]
        sorted_ = sorted(objs)
        result = [str(o) for o in sorted_]
        self.assertEqual(result, req, msg=f"{unsorted=}")

    def test_valid__init__(self):
        """SwVersion.__init__()"""
        v0 = dict(public="0", base_version="0", release=(0,),
                  major=0, minor=0, micro=0, nano=0)
        v1 = dict(public="1", base_version="1", release=(1,),
                  major=1, minor=0, micro=0, nano=0)
        v2 = dict(public="1.2", base_version="1.2", release=(1, 2),
                  major=1, minor=2, micro=0, nano=0)
        v3 = dict(public="1.2.3", base_version="1.2.3", release=(1, 2, 3),
                  major=1, minor=2, micro=3, nano=0)
        v4 = dict(public="11.22.33.44", base_version="11.22.33.44", release=(11, 22, 33, 44),
                  major=11, minor=22, micro=33, nano=44)
        v5 = dict(public="11.22.33.44.55", base_version="11.22.33.44", release=(11, 22, 33, 44),
                  major=11, minor=22, micro=33, nano=44)
        cisco1 = dict(public="11.22(33)se", base_version="11.22.33", release=(11, 22, 33),
                      major=11, minor=22, micro=33, nano=0)
        cisco2 = dict(public="11.22(33)se44", base_version="11.22.33.44", release=(11, 22, 33, 44),
                      major=11, minor=22, micro=33, nano=44)
        for text, req, req_d in [
            ("", "0", v0),
            ("0", "0", v0),
            (0, "0", v0),
            ("1", "1", v1),
            (1, "1", v1),
            ("1.2", "1.2", v2),
            ("1.2.3", "1.2.3", v3),
            ("11.22.33.44", "11.22.33.44", v4),
            ("11.22.33.44.55", "11.22.33.44.55", v5),
            # cisco
            ("11.22(33)SE", "11.22(33)se", cisco1),
            ("11.22(33)SE44", "11.22(33)se44", cisco2),
        ]:
            obj = SwVersion(text)

            result = str(obj)
            self.assertEqual(result, req, msg=f"{text=}")
            self._test_attrs(obj=obj, req_d=req_d, msg=f"{text=}")


if __name__ == "__main__":
    unittest.main()
