"""Tests tcp.py"""

import unittest

from netports import tcp, NetportsValueError

ALL = list(range(1, 65536))


# noinspection DuplicatedCode
class Test(unittest.TestCase):
    """Tests tcp.py"""

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
            (dict(items=0), NetportsValueError),
            (dict(items="0"), NetportsValueError),
            (dict(items=[0]), NetportsValueError),
            (dict(items=65536), NetportsValueError),
            (dict(items="65536"), NetportsValueError),
            (dict(items=[65536]), NetportsValueError),
            # typo
            (dict(items="typo"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                tcp.itcp(**kwargs)
            with self.assertRaises(error, msg=f"{kwargs=}"):
                tcp.stcp(**kwargs)

    def test__check_port(self):
        """check_port()"""
        for kwargs, req in [
            ({"port": "", "strict": True}, TypeError),
            ({"port": "", "strict": False}, TypeError),
            ({"port": {}, "strict": True}, TypeError),
            ({"port": {}, "strict": False}, TypeError),
            ({"port": "-1", "strict": True}, TypeError),
            ({"port": "-1", "strict": False}, TypeError),
            ({"port": -1, "strict": True}, NetportsValueError),
            ({"port": -1, "strict": False}, False),
            ({"port": "0", "strict": True}, TypeError),
            ({"port": "0", "strict": False}, TypeError),
            ({"port": 0, "strict": True}, NetportsValueError),
            ({"port": 0, "strict": False}, False),
            ({"port": "1", "strict": True}, TypeError),
            ({"port": "1", "strict": False}, TypeError),
            ({"port": 1, "strict": True}, True),
            ({"port": 1, "strict": False}, True),
            ({"port": "65535", "strict": True}, TypeError),
            ({"port": "65535", "strict": False}, TypeError),
            ({"port": 65535, "strict": True}, True),
            ({"port": 65535, "strict": False}, True),
            ({"port": "65536", "strict": True}, TypeError),
            ({"port": "65536", "strict": False}, TypeError),
            ({"port": 65536, "strict": True}, NetportsValueError),
            ({"port": 65536, "strict": False}, False),
        ]:
            if isinstance(req, bool):
                result = tcp.check_port(**kwargs)
                self.assertEqual(result, req, msg=f"{kwargs=}")
            else:
                with self.assertRaises(req, msg=f"{kwargs=}"):
                    tcp.check_port(**kwargs)

    def test__check_ports(self):
        """check_ports()"""
        for kwargs, req in [
            ({"ports": [], "strict": True}, True),
            ({"ports": [], "strict": False}, True),
            ({"ports": ["1"], "strict": True}, TypeError),
            ({"ports": ["1"], "strict": False}, TypeError),
            ({"ports": [1, 65535], "strict": True}, True),
            ({"ports": [1, 65535], "strict": False}, True),
            ({"ports": ["0"], "strict": True}, TypeError),
            ({"ports": ["0"], "strict": False}, TypeError),
        ]:
            if isinstance(req, bool):
                result = tcp.check_ports(**kwargs)
                self.assertEqual(result, req, msg=f"{kwargs=}")
            else:
                with self.assertRaises(req, msg=f"{kwargs=}"):
                    tcp.check_ports(**kwargs)


if __name__ == "__main__":
    unittest.main()
