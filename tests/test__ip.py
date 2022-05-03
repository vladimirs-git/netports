"""unittest ip.py"""

import unittest

from netports import ip

ALL_IP = list(range(0, 256))


class Test(unittest.TestCase):
    """unittest ip.py"""

    def test_valid__iip(self):
        """iip()"""
        for items, req in [
            ("", []),
            ([], []),
            (0, [0]),
            (255, [255]),
            ([0, 255, 1], [0, 1, 255]),
            ("3-5,0", [0, 3, 4, 5]),
            ("icmp", [1]),
            ("icmp,1,icmp,1,7,3-5,3-4,udp,17,igmp", [1, 2, 3, 4, 5, 7, 17]),
            ("ip", ALL_IP),
            ("ip,icmp,2", ALL_IP),
        ]:
            result = ip.iip(items)
            self.assertEqual(result, req, msg=f"{items=}")

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

    def test_valid__iip_all(self):
        """iip_all()"""
        result = ip.iip_all()
        req = ALL_IP
        self.assertEqual(result, req, msg="iip_all")

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
        for items, req in [
            ("", ""),
            ([], ""),
            (0, "0"),
            ([255], "255"),
            ([5, 5, 1, 3, 4], "1,3-5"),
            ("3-4,3-5,17,icmp,udp", "1,3-5,17"),
            (["icmp", "tcp", "7", 255], "1,6-7,255"),
        ]:
            result = ip.sip(items)
            self.assertEqual(result, req, msg=f"{items=}")

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

    def test_valid__sip_all(self):
        """sip_all()"""
        result = ip.sip_all()
        req = "0-255"
        self.assertEqual(result, req, msg="sip_all")


if __name__ == "__main__":
    unittest.main()
