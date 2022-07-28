"""unittest ip.py"""

import unittest

from netports import ip

ALL = list(range(0, 256))


class Test(unittest.TestCase):
    """unittest ip.py"""

    def test_valid__iip(self):
        """iip()"""
        for kwargs, req, req_ in [
            # ports
            ({}, [], ""),
            (dict(items=""), [], ""),
            (dict(items=[]), [], ""),
            (dict(items=0), [0], "0"),
            (dict(items="0"), [0], "0"),
            (dict(items=[0]), [0], "0"),
            (dict(items=255), [255], "255"),
            (dict(items=[5, 5, 0, 3, 4]), [0, 3, 4, 5], "0,3-5"),
            (dict(items="3-5,0,3-4,0"), [0, 3, 4, 5], "0,3-5"),
            (dict(items="1,256", strict=False), [1], "1"),
            # name
            (dict(items="icmp"), [1], "1"),
            (dict(items=["icmp"]), [1], "1"),
            (dict(items="icmp,tcp"), [1, 6], "1,6"),
            (dict(items=["icmp", "tcp"]), [1, 6], "1,6"),
            (dict(items="icmp,1,icmp,1,5,3-4,tcp"), [1, 3, 4, 5, 6], "1,3-6"),
            (dict(items="icmp,typo", strict=False), [1], "1"),
            # 0-255
            (dict(items="0-255"), [-1], "0-255"),
            (dict(items=ALL), [-1], "0-255"),
            (dict(items=ALL, verbose=False), [-1], "0-255"),
            (dict(items=ALL, verbose=True), ALL, "0-255"),
            (dict(items="0-255,1"), [-1], "0-255"),
            (dict(items=[*ALL, 1]), [-1], "0-255"),
            (dict(items="0-255,icmp"), [-1], "0-255"),
            (dict(items=[*ALL, "icmp"]), [-1], "0-255"),
            (dict(items=[*ALL, 256, "typo"], strict=False), [-1], "0-255"),
            # -1
            (dict(items=-1), [-1], "0-255"),
            (dict(items="-1"), [-1], "0-255"),
            (dict(items=[-1]), [-1], "0-255"),
            (dict(items=["-1"]), [-1], "0-255"),
            (dict(items=[-1, 2]), [-1], "0-255"),
            (dict(items=["-1", "2"]), [-1], "0-255"),
            (dict(items=[-1], verbose=False), [-1], "0-255"),
            (dict(items=["-1", 256, "typo"], strict=False), [-1], "0-255"),
            # all
            (dict(all=True), [-1], "0-255"),
            (dict(all=True, verbose=False), [-1], "0-255"),
            (dict(all=True, verbose=True), ALL, "0-255"),
            (dict(items="1", all=True), [-1], "0-255"),
            (dict(items="1", all=True, verbose=False), [-1], "0-255"),
            (dict(items="1", all=True, verbose=True), ALL, "0-255"),
            # combo
            (dict(items="1,ipinip,255"), [1, 4, 255], "1,4,255"),
            (dict(items="1,ipinip,255,256,typo", strict=False), [1, 4, 255], "1,4,255"),
        ]:
            result = ip.iip(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")
            result_ = ip.sip(**kwargs)
            self.assertEqual(result_, req_, msg=f"{kwargs=}")

    def test_invalid__iip(self):
        """iip()"""
        for kwargs, error in [
            # ports
            (dict(items=256), ValueError),
            (dict(items="256"), ValueError),
            (dict(items=[256]), ValueError),
            # typo
            (dict(items="typo"), ValueError),
        ]:
            with self.assertRaises(error, msg=f"{kwargs=}"):
                ip.iip(**kwargs)
            with self.assertRaises(error, msg=f"{kwargs=}"):
                ip.sip(**kwargs)

    def test_ip_pairs(self):
        """ip_pairs()"""
        for kwargs, req in [
            # ports
            (dict(items=""), ([], [])),
            (dict(items=[]), ([], [])),
            (dict(items="1"), ([(1, "icmp")], [])),
            (dict(items=1), ([(1, "icmp")], [])),
            (dict(items=["1"]), ([(1, "icmp")], [])),
            (dict(items=[1]), ([(1, "icmp")], [])),
            (dict(items="255"), ([(255, "")], [])),
            # name
            (dict(items="icmp"), ([(1, "icmp")], [])),
            (dict(items=["icmp"]), ([(1, "icmp")], [])),
            (dict(items="tcp,icmp"), ([(1, "icmp"), (6, "tcp")], [])),
            (dict(items=["tcp", "icmp"]), ([(1, "icmp"), (6, "tcp")], [])),
            # alias
            (dict(items="ipinip"), ([(4, "ipinip")], [])),
            (dict(items="ip-in-ip"), ([(4, "ip-in-ip")], [])),
            (dict(items=4), ([(4, "ip-in-ip")], [])),
            (dict(items=["ipinip", "ip-in-ip"]), ([(4, "ip-in-ip")], [])),
            (dict(items=["ip-in-ip", "ipinip"]), ([(4, "ip-in-ip")], [])),
            # 0-255
            (dict(items="0-255"), ([(-1, "ip")], [])),
            (dict(items=ALL), ([(-1, "ip")], [])),
            (dict(items=ALL, verbose=False), ([(-1, "ip")], [])),
            (dict(items=ALL, verbose=True), (ip.ALL_PAIRS, [])),
            # -1
            (dict(items=-1), ([(-1, "ip")], [])),
            (dict(items="-1"), ([(-1, "ip")], [])),
            (dict(items=[-1]), ([(-1, "ip")], [])),
            (dict(items=["-1"]), ([(-1, "ip")], [])),
            (dict(items=[-1, 2]), ([(-1, "ip")], [])),
            (dict(items=["-1", "2"]), ([(-1, "ip")], [])),
            (dict(items=[-1], verbose=False), ([(-1, "ip")], [])),
            # ip
            (dict(items="ip"), ([(-1, "ip")], [])),
            (dict(items="ip", verbose=False), ([(-1, "ip")], [])),
            (dict(items="ip", verbose=True), (ip.ALL_PAIRS, [])),
            (dict(items="ip,icmp"), ([(-1, "ip")], [])),
            (dict(items=["ip", "icmp"]), ([(-1, "ip")], [])),
            (dict(items=["ip", "icmp"], verbose=True), (ip.ALL_PAIRS, [])),
            # undefined
            (dict(items=["typo"]), ([], ["typo"])),
            (dict(items=[256]), ([], ["256"])),
            (dict(items=["typo", 256, 1]), ([(1, "icmp")], ["256", "typo"])),
            (dict(items=[*ALL, 256]), ([(-1, "ip")], ["256"])),
            (dict(items=[*ALL, 256], verbose=True), (ip.ALL_PAIRS, ["256"])),
            # combo
            (dict(items="typo,1,ipinip,255,256"),
             ([(1, "icmp"), (4, "ipinip"), (255, "")], ["256", "typo"])),
            (dict(items="ipinip,ip-in-ip"), ([(4, "ip-in-ip")], [])),
        ]:
            result = ip.ip_pairs(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")


if __name__ == "__main__":
    unittest.main()
