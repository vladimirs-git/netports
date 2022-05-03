"""unittest tcp.py"""

import unittest

from netports import tcp


class Test(unittest.TestCase):
    """unittest tcp.py"""

    def test_valid__itcp(self):
        """itcp()"""
        for kwargs, req in [
            (dict(), []),
            (dict(items=""), []),
            (dict(items=[]), []),
            (dict(items=1), [1]),
            (dict(items="1"), [1]),
            (dict(items=[1]), [1]),
            (dict(items=[65535]), [65535]),
            (dict(items=[5, 5, 1, 3, 4]), [1, 3, 4, 5]),
            (dict(items="3-5,1,3-5,1"), [1, 3, 4, 5]),
            (dict(all=True), list(range(1, 65536))),
            (dict(items="1", all=True), list(range(1, 65536))),
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
            (dict(), ""),
            (dict(items=""), ""),
            (dict(items=[]), ""),
            (dict(items="1"), "1"),
            (dict(items=1), "1"),
            (dict(items=[1]), "1"),
            (dict(items=[65535]), "65535"),
            (dict(items=[5, 5, 1, 3, 4]), "1,3-5"),
            (dict(items="3-5,1,3-5,1"), "1,3-5"),
            (dict(all=True), "1-65535"),
            (dict(items="1", all=True), "1-65535"),
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
