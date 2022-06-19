"""unittest tcp.py"""

import unittest

from netports import tcp

ALL_TCP = list(range(1, 65536))


class Test(unittest.TestCase):
    """unittest tcp.py"""

    def test_valid__itcp(self):
        """itcp()"""
        for kwargs, req in [
            ({}, []),
            (dict(items=""), []),
            (dict(items=[]), []),
            (dict(items=1), [1]),
            (dict(items="1"), [1]),
            (dict(items=[1]), [1]),
            (dict(items=[65535]), [65535]),
            (dict(items=[5, 5, 1, 3, 4]), [1, 3, 4, 5]),
            (dict(items="3-5,1,3-5,1"), [1, 3, 4, 5]),

            (dict(items=ALL_TCP), ALL_TCP),
            (dict(items=ALL_TCP, verbose=True), ALL_TCP),
            (dict(items=ALL_TCP, verbose=False), [-1]),

            (dict(all=True), ALL_TCP),
            (dict(all=True, verbose=True), ALL_TCP),
            (dict(all=True, verbose=False), [-1]),
            (dict(items="1", all=True), ALL_TCP),
            (dict(items="1", all=True, verbose=True), ALL_TCP),
            (dict(items="1", all=True, verbose=False), [-1]),

            (dict(items="-1", verbose=False), [-1]),
            (dict(items=["-1"], verbose=False), [-1]),
            (dict(items=["-1", "2"], verbose=False), [-1]),
            (dict(items=["typo", "-1"], verbose=False), [-1]),
            (dict(items=-1, verbose=False), [-1]),
            (dict(items=[-1], verbose=False), [-1]),
            (dict(items=[-1, 2], verbose=False), [-1]),
            (dict(items=[-2, -1], verbose=False), [-1]),
        ]:
            result = tcp.itcp(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__itcp(self):
        """itcp()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("65536", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([65536], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                tcp.itcp(items)

    def test_valid__stcp(self):
        """stcp()"""
        for kwargs, req in [
            ({}, ""),
            (dict(items=""), ""),
            (dict(items=[]), ""),
            (dict(items="1"), "1"),
            (dict(items=1), "1"),
            (dict(items=[1]), "1"),
            (dict(items=[65535]), "65535"),
            (dict(items=[5, 5, 1, 3, 4]), "1,3-5"),
            (dict(items="3-5,1,3-5,1"), "1,3-5"),

            (dict(items=ALL_TCP), "1-65535"),
            (dict(items=ALL_TCP, verbose=True), "1-65535"),
            (dict(items=ALL_TCP, verbose=False), "1-65535"),

            (dict(all=True), "1-65535"),
            (dict(all=True, verbose=True), "1-65535"),
            (dict(all=True, verbose=False), "1-65535"),
            (dict(items="1", all=True), "1-65535"),
            (dict(items="1", all=True, verbose=True), "1-65535"),
            (dict(items="1", all=True, verbose=False), "1-65535"),

            (dict(items="-1", verbose=False), "1-65535"),
            (dict(items=["-1"], verbose=False), "1-65535"),
            (dict(items=["-1", "2"], verbose=False), "1-65535"),
            (dict(items=["typo", "-1"], verbose=False), "1-65535"),
            (dict(items=-1, verbose=False), "1-65535"),
            (dict(items=[-1], verbose=False), "1-65535"),
            (dict(items=[-1, 2], verbose=False), "1-65535"),
            (dict(items=[-2, -1], verbose=False), "1-65535"),
        ]:
            result = tcp.stcp(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__stcp(self):
        """stcp()"""
        for items, error in [
            ("-1", ValueError),
            ("0", ValueError),
            ("65536", ValueError),
            ([0], ValueError),
            ([-1], ValueError),
            ([65536], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                tcp.stcp(items)


if __name__ == "__main__":
    unittest.main()
