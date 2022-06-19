"""unittest ip.py"""

import unittest

from netports import ip

ALL_IP = list(range(0, 256))


class Test(unittest.TestCase):
    """unittest ip.py"""

    def test_valid__iip(self):
        """iip()"""
        for kwargs, req in [
            ({}, []),
            (dict(items=""), []),
            (dict(items=[]), []),
            (dict(items=0), [0]),
            (dict(items="0"), [0]),
            (dict(items=[0]), [0]),
            (dict(items=255), [255]),
            (dict(items=[5, 5, 0, 3, 4]), [0, 3, 4, 5]),
            (dict(items="3-5,0,3-4,0"), [0, 3, 4, 5]),
            (dict(items="icmp"), [1]),
            (dict(items="icmp,1,icmp,1,7,3-5,3-4,udp"), [1, 3, 4, 5, 7, 17]),

            (dict(items="ip"), ALL_IP),
            (dict(items="ip", verbose=True), ALL_IP),
            (dict(items="ip", verbose=False), [-1]),
            (dict(items="ip,icmp,2"), ALL_IP),
            (dict(items="ip,icmp,2", verbose=True), ALL_IP),
            (dict(items="ip,icmp,2", verbose=False), [-1]),
            (dict(items=ALL_IP), ALL_IP),
            (dict(items=ALL_IP, verbose=True), ALL_IP),
            (dict(items=ALL_IP, verbose=False), [-1]),

            (dict(all=True), ALL_IP),
            (dict(all=True, verbose=True), ALL_IP),
            (dict(all=True, verbose=False), [-1]),
            (dict(items="1", all=True), ALL_IP),
            (dict(items="1", all=True, verbose=True), ALL_IP),
            (dict(items="1", all=True, verbose=False), [-1]),

            (dict(items="-1", verbose=False), [-1]),
            (dict(items=["-1"], verbose=False), [-1]),
            (dict(items=["-1", "2"], verbose=False), [-1]),
            (dict(items=["typo", "-1"], verbose=False), [-1]),
            (dict(items=-1, verbose=False), [-1]),
            (dict(items=[-1], verbose=False), [-1]),
            (dict(items=[-1, 2], verbose=False), [-1]),
            (dict(items=[-2, -1], verbose=False), [-1]),

            (dict(items="-1,1,1,256,typo", strict=False), [1]),
        ]:
            result = ip.iip(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__iip(self):
        """iip()"""
        for items, error in [
            ("-1", ValueError),
            ("256", ValueError),
            ([-1], ValueError),
            ([265], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ip.iip(items)

    def test_nip(self):
        """nip()"""
        for kwargs, req in [
            (dict(items=""), ([], [])),
            (dict(items=[]), ([], [])),
            (dict(items="1"), ([], [1])),
            (dict(items=1), ([], [1])),
            (dict(items=["1"]), ([], [1])),
            (dict(items=[1]), ([], [1])),
            (dict(items=ALL_IP), ([], ALL_IP)),
            (dict(items="icmp"), (["icmp"], [])),
            (dict(items="icmp,1"), (["icmp"], [1])),

            (dict(items="ip"), (["ip"], ALL_IP)),
            (dict(items=["ip", "icmp"]), (["ip"], ALL_IP)),
            (dict(items="ip,icmp"), (["ip"], ALL_IP)),
            (dict(items=["ip", *ALL_IP]), (["ip"], ALL_IP)),

            (dict(items="tcp,2,3-5,1,icmp"), (["icmp", "tcp"], [1, 2, 3, 4, 5])),
            (dict(items=["tcp", "2", "3-5", "1", "icmp"]), (["icmp", "tcp"], [1, 2, 3, 4, 5])),
            (dict(items=["tcp,typo,1,226"], strict=False), (["tcp", "typo"], [1, 226])),
        ]:
            result = ip.nip(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__nip(self):
        """nip()"""
        for kwargs, error in [
            (dict(items="-1"), ValueError),
            (dict(items="256"), ValueError),
            (dict(items=[-1]), ValueError),
            (dict(items=[256]), ValueError),
            (dict(items="typo"), ValueError),
            (dict(items="typo", strict=True), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                ip.nip(**kwargs)

    def test_valid__sip(self):
        """sip()"""
        for kwargs, req in [
            ({}, ""),
            (dict(items=""), ""),
            (dict(items=[]), ""),
            (dict(items=0), "0"),
            (dict(items="0"), "0"),
            (dict(items=[0]), "0"),
            (dict(items=[255]), "255"),
            (dict(items=[5, 5, 0, 3, 4]), "0,3-5"),
            (dict(items="3-5,0,3-4,0"), "0,3-5"),
            (dict(items="icmp"), "1"),
            (dict(items="icmp,1,icmp,1,7,3-5,3-4,udp"), "1,3-5,7,17"),

            (dict(items="ip"), "0-255"),
            (dict(items="ip", verbose=True), "0-255"),
            (dict(items="ip", verbose=False), "0-255"),
            (dict(items="ip,icmp,2"), "0-255"),
            (dict(items="ip,icmp,2", verbose=True), "0-255"),
            (dict(items="ip,icmp,2", verbose=False), "0-255"),
            (dict(items=ALL_IP), "0-255"),
            (dict(items=ALL_IP, verbose=True), "0-255"),
            (dict(items=ALL_IP, verbose=False), "0-255"),

            (dict(all=True), "0-255"),
            (dict(all=True, verbose=True), "0-255"),
            (dict(all=True, verbose=False), "0-255"),
            (dict(items="1", all=True), "0-255"),
            (dict(items="1", all=True, verbose=True), "0-255"),
            (dict(items="1", all=True, verbose=False), "0-255"),

            (dict(items="-1", verbose=False), "0-255"),
            (dict(items=["-1"], verbose=False), "0-255"),
            (dict(items=["-1", "2"], verbose=False), "0-255"),
            (dict(items=["typo", "-1"], verbose=False), "0-255"),
            (dict(items=-1, verbose=False), "0-255"),
            (dict(items=[-1], verbose=False), "0-255"),
            (dict(items=[-1, 2], verbose=False), "0-255"),
            (dict(items=[-2, -1], verbose=False), "0-255"),
        ]:
            result = ip.sip(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_invalid__sip(self):
        """sip()"""
        for items, error in [
            ("-1", ValueError),
            ("256", ValueError),
            ([-1], ValueError),
            ([256], ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ip.sip(items)


if __name__ == "__main__":
    unittest.main()
