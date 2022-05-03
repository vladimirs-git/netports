"""unittest tcp.py"""

import unittest

from netports import tcp


class Test(unittest.TestCase):
    """unittest tcp.py"""

    def test_valid__itcp(self):
        """itcp()"""
        for items, req in [
            ("", []),
            ([], []),
            (1, [1]),
            ([65535], [65535]),
            ([1, 3, 4, 5], [1, 3, 4, 5]),
            ("1,3-5", [1, 3, 4, 5]),
        ]:
            result = tcp.itcp(items)
            self.assertEqual(result, req, msg=f"{items=}")

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

    def test_valid__itcp_all(self):
        """itcp_all()"""
        result = tcp.itcp_all()
        req = list(range(1, 65536))
        self.assertEqual(result, req, msg="itcp_all")

    def test_valid__stcp(self):
        """stcp()"""
        for items, req in [
            ("", ""),
            ([], ""),
            (1, "1"),
            ([65535], "65535"),
            ([1, 3, 4, 5], "1,3-5"),
            ("1,3-5", "1,3-5"),
        ]:
            result = tcp.stcp(items)
            self.assertEqual(result, req, msg=f"{items=}")

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

    def test_valid__stcp_all(self):
        """stcp_all()"""
        result = tcp.stcp_all()
        req = "1-65535"
        self.assertEqual(result, req, msg="stcp_all")


if __name__ == "__main__":
    unittest.main()
