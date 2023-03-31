"""unittest vlan.py"""

import unittest

import dictdiffer  # type: ignore

from netports import vlan, NetportsValueError

ALL = list(range(1, 4095))


class Test(unittest.TestCase):
    """unittest vlan.py"""

    def test_valid__ivlan__svlan(self):
        """ivlan() svlan()"""
        for kwargs, req, req_ in [
            # vlans
            ({}, [], ""),
            (dict(items=""), [], ""),
            (dict(items=[]), [], ""),
            (dict(items=1), [1], "1"),
            (dict(items="1"), [1], "1"),
            (dict(items=[1]), [1], "1"),
            (dict(items=["1"]), [1], "1"),
            (dict(items=[4094]), [4094], "4094"),
            (dict(items=[5, 5, 1, 3, 4]), [1, 3, 4, 5], "1,3-5"),
            (dict(items="3-5,1,3-5,1"), [1, 3, 4, 5], "1,3-5"),
            # 1-4094
            (dict(items="1-4094"), [-1], "1-4094"),
            (dict(items=ALL), [-1], "1-4094"),
            (dict(items=ALL, verbose=False), [-1], "1-4094"),
            (dict(items=ALL, verbose=True), ALL, "1-4094"),
            (dict(items="1-4094,1"), [-1], "1-4094"),
            (dict(items=[*ALL, 1]), [-1], "1-4094"),
            # -1
            (dict(items=-1), [-1], "1-4094"),
            (dict(items="-1"), [-1], "1-4094"),
            (dict(items=[-1]), [-1], "1-4094"),
            (dict(items=["-1"]), [-1], "1-4094"),
            (dict(items=[-1, 2]), [-1], "1-4094"),
            (dict(items=["-1", "2"]), [-1], "1-4094"),
            (dict(items=[-1], verbose=False), [-1], "1-4094"),
            # all
            (dict(all=True), [-1], "1-4094"),
            (dict(all=True, verbose=False), [-1], "1-4094"),
            (dict(all=True, verbose=True), ALL, "1-4094"),
            (dict(items="1", all=True), [-1], "1-4094"),
            (dict(items="1", all=True, verbose=False), [-1], "1-4094"),
            (dict(items="1", all=True, verbose=True), ALL, "1-4094"),
            # splitter
            (dict(items="1,3-5", platform="cisco"), [1, 3, 4, 5], "1,3-5"),
            (dict(items="1 3 to 5", platform="hpe"), [1, 3, 4, 5], "1 3 to 5"),
            (dict(items="1,3-5", splitter=",", range_splitter="-"), [1, 3, 4, 5], "1,3-5"),
            (dict(items="1 3 to 5", splitter=" ", range_splitter=" to "), [1, 3, 4, 5], "1 3 to 5"),
            # splitter -1
            (dict(items="-1", platform="cisco"), [-1], "1-4094"),
            (dict(items="-1", platform="hpe"), [-1], "1 to 4094"),
            (dict(items="-1", splitter=",", range_splitter="-"), [-1], "1-4094"),
            (dict(items="-1", splitter=" ", range_splitter=" to "), [-1], "1 to 4094"),
        ]:
            result = vlan.ivlan(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")
            result_ = vlan.svlan(**kwargs)
            self.assertEqual(result_, req_, msg=f"{kwargs=}")

    def test_invalid__ivlan__svlan(self):
        """ivlan() svlan()"""
        for kwargs, error in [
            # vlans
            (dict(items=0), NetportsValueError),
            (dict(items="0"), NetportsValueError),
            (dict(items=[0]), NetportsValueError),
            (dict(items=4095), NetportsValueError),
            (dict(items="4095"), NetportsValueError),
            (dict(items=[4095]), NetportsValueError),
            # typo
            (dict(items="typo"), ValueError),
            # splitter
            (dict(items="1,3-5", platform="hpe"), NetportsValueError),
            (dict(items="1 3 to 5", platform="cisco"), NetportsValueError),
            # splitter -1 verbose
            (dict(items="-1", verbose=True, platform="cisco"), NetportsValueError),
            (dict(items="-1", verbose=True, platform="hpe"), NetportsValueError),
            (dict(items="-1", verbose=True, splitter=",", range_splitter="-"), NetportsValueError),
            (dict(items="-1", verbose=True, splitter=" ", range_splitter=" to "),
             NetportsValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                vlan.ivlan(**kwargs)
            with self.assertRaises(error, msg=f"{kwargs=}"):
                vlan.svlan(**kwargs)

    # =========================== helpers ============================

    def test_valid__replace_range_splitter(self):
        """_replace_range_splitter()"""
        for item, kwargs, req in [
            ("", {}, ""),
            ("1-3", {}, "1-3"),
            ("1-3", dict(range_splitter=" to "), "1 to 3"),
            ("1-3", dict(splitter=" to "), "1-3"),
        ]:
            result = vlan._replace_range_splitter(item=item, **kwargs)
            self.assertEqual(result, req, msg=f"{item=} {kwargs=}")

    def test_valid__update_splitters(self):
        """_update_splitters()"""
        for kwargs, req_d in [
            ({}, {}),
            (dict(splitter="a", range_splitter="a"), dict(splitter="a", range_splitter="a")),
            (dict(platform="cisco"), dict(platform="cisco", splitter=",", range_splitter="-")),
            (dict(platform="cisco", splitter="a", range_splitter="a"),
             dict(platform="cisco", splitter=",", range_splitter="-")),
            (dict(platform="hpe", splitter="a", range_splitter="a"),
             dict(platform="hpe", splitter=" ", range_splitter=" to ")),
        ]:
            result = vlan._update_splitters(**kwargs)
            diff = list(dictdiffer.diff(result, req_d))
            self.assertEqual(diff, [], msg=f"{kwargs=}")


if __name__ == "__main__":
    unittest.main()
