"""unittest ip.py"""

import unittest

from netports import ip

ALL_IP = list(range(0, 256))


class Test(unittest.TestCase):
    """unittest ip.py"""

    def test_valid__iip(self):
        """iip()"""
        for kwargs, req in [
            (dict(), []),
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
            (dict(items="ip,icmp,2"), ALL_IP),
            (dict(all=True), ALL_IP),
            (dict(items="1", all=True), ALL_IP),
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

    def test_iip_nip(self):
        """iip_nip()"""
        for items, req in [
            ("", ([], [])),
            ([], ([], [])),
            ("1", ([1], [])),
            ("icmp", ([], ["icmp"])),
            ("icmp,1", ([1], ["icmp"])),
            ("ip", (ALL_IP, ["ip"])),
            (["ip", "icmp"], (ALL_IP, ["ip"])),
            ("ip,icmp", (ALL_IP, ["ip"])),
            ("tcp,2,3-5,1,icmp", ([1, 2, 3, 4, 5], ["icmp", "tcp"])),
            (["tcp", "2", "3-5", "1", "icmp"], ([1, 2, 3, 4, 5], ["icmp", "tcp"])),
        ]:
            result = ip.iip_nip(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__iip_nip(self):
        """iip_nip()"""
        for items, error in [
            ("-1", ValueError),
            ("256", ValueError),
            ([-1], ValueError),
            ([256], ValueError),
            ("typo", ValueError),
        ]:
            with self.assertRaises(error, msg=f"{items=}"):
                ip.iip_nip(items)

    def test_valid__sip(self):
        """sip()"""
        for kwargs, req in [
            (dict(), ""),
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
            (dict(items="ip,icmp,2"), "0-255"),
            (dict(all=True), "0-255"),
            (dict(items="1", all=True), "0-255"),
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
