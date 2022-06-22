"""unittest tcp.py"""

import unittest

from netports import tcp

ALL = list(range(1, 65536))


# noinspection DuplicatedCode
class Test(unittest.TestCase):
    """unittest tcp.py"""

    def test_valid__itcp__stcp(self):
        """itcp() stcp()"""
        for kwargs, req, req_ in [
            # ports
            ({}, [], ""),
            (dict(items=""), [], ""),
            (dict(items=[]), [], ""),
            (dict(items=1), [1], "1"),
            (dict(items="1"), [1], "1"),
            (dict(items=[1]), [1], "1"),
            (dict(items=["1"]), [1], "1"),
            (dict(items=[65535]), [65535], "65535"),
            (dict(items=[5, 5, 1, 3, 4]), [1, 3, 4, 5], "1,3-5"),
            (dict(items="3-5,1,3-5,1"), [1, 3, 4, 5], "1,3-5"),
            # 1-65535
            (dict(items="1-65535"), [-1], "1-65535"),
            (dict(items=ALL), [-1], "1-65535"),
            (dict(items=ALL, verbose=False), [-1], "1-65535"),
            (dict(items=ALL, verbose=True), ALL, "1-65535"),
            (dict(items="1-65535,1"), [-1], "1-65535"),
            (dict(items=[*ALL, 1]), [-1], "1-65535"),
            # -1
            (dict(items=-1), [-1], "1-65535"),
            (dict(items="-1"), [-1], "1-65535"),
            (dict(items=[-1]), [-1], "1-65535"),
            (dict(items=["-1"]), [-1], "1-65535"),
            (dict(items=[-1, 2]), [-1], "1-65535"),
            (dict(items=["-1", "2"]), [-1], "1-65535"),
            (dict(items=[-1], verbose=False), [-1], "1-65535"),
            # all
            (dict(all=True), [-1], "1-65535"),
            (dict(all=True, verbose=False), [-1], "1-65535"),
            (dict(all=True, verbose=True), ALL, "1-65535"),
            (dict(items="1", all=True), [-1], "1-65535"),
            (dict(items="1", all=True, verbose=False), [-1], "1-65535"),
            (dict(items="1", all=True, verbose=True), ALL, "1-65535"),
        ]:
            result = tcp.itcp(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")
            result_ = tcp.stcp(**kwargs)
            self.assertEqual(result_, req_, msg=f"{kwargs=}")

    def test_invalid__itcp__stcp(self):
        """itcp() stcp()"""
        for kwargs, error in [
            # ports
            (dict(items=0), ValueError),
            (dict(items="0"), ValueError),
            (dict(items=[0]), ValueError),
            (dict(items=65536), ValueError),
            (dict(items="65536"), ValueError),
            (dict(items=[65536]), ValueError),
            # typo
            (dict(items="typo"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                tcp.itcp(**kwargs)
            with self.assertRaises(error, msg=f"{kwargs=}"):
                tcp.stcp(**kwargs)


if __name__ == "__main__":
    unittest.main()
