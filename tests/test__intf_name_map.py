"""unittest intf_name_map.py"""

import unittest

from netports import intf_name_map


class Test(unittest.TestCase):
    """unittest intf_name_map.py"""

    # ============================= str ==============================

    def test_valid__long_to_shorts(self):
        """intf_name_map.long_to_shorts"""
        for long, expected in [
            ("FastEthernet", ["Fa"]),
            ("GigabitEthernet", ["Gi"]),
            ("TenGigabitEthernet", ["Te"]),
            ("Ethernet", ["Eth"]),
            ("Tunnel-ip", ["Tu"]),
            ("Tunnel", ["Tu"]),
            ("Port-channel", ["Po"]),
            ("Loopback", ["Lo"]),
            ("Vlan", ["V", "Vl"]),
        ]:
            actual = intf_name_map.long_to_shorts[long]
            self.assertEqual(expected, actual, msg=f"{long=}")

    def test_valid__long_to_short(self):
        """intf_name_map.long_to_short"""
        for long, expected in [
            ("FastEthernet", "Fa"),
            ("GigabitEthernet", "Gi"),
            ("TenGigabitEthernet", "Te"),
            ("Ethernet", "Eth"),
            ("Tunnel-ip", "Tu"),
            ("Tunnel", "Tu"),
            ("Port-channel", "Po"),
            ("Loopback", "Lo"),
            ("Vlan", "V"),
        ]:
            actual = intf_name_map.long_to_short[long]
            self.assertEqual(expected, actual, msg=f"{long=}")

    def test_valid__long_to_short_lower(self):
        """intf_name_map.long_to_short_lower"""
        for long, expected in [
            ("fastethernet", "Fa"),
            ("gigabitethernet", "Gi"),
            ('tengigabitethernet', "Te"),
            ("ethernet", "Eth"),
            ("tunnel-ip", "Tu"),
            ("tunnel", "Tu"),
            ("port-channel", "Po"),
            ("loopback", "Lo"),
            ("vlan", "V"),
        ]:
            actual = intf_name_map.long_to_short_lower[long]
            self.assertEqual(expected, actual, msg=f"{long=}")

    def test_valid__short_to_long(self):
        """intf_name_map.short_to_long"""
        for long, expected in [
            ("Fa", "FastEthernet"),
            ("Gi", "GigabitEthernet"),
            ("Te", "TenGigabitEthernet"),
            ("Eth", "Ethernet"),
            ("Tu", "Tunnel"),
            ("Po", "Port-channel"),
            ("Lo", "Loopback"),
            ("Vl", "Vlan"),
        ]:
            actual = intf_name_map.short_to_long[long]
            self.assertEqual(expected, actual, msg=f"{long=}")

    def test_valid__short_to_long_lower(self):
        """intf_name_map.short_to_long_lower"""
        for long, expected in [
            ("fa", "FastEthernet"),
            ("gi", "GigabitEthernet"),
            ("te", "TenGigabitEthernet"),
            ("eth", "Ethernet"),
            ("tu", "Tunnel"),
            ("po", "Port-channel"),
            ("lo", "Loopback"),
            ("vl", "Vlan"),
        ]:
            actual = intf_name_map.short_to_long_lower[long]
            self.assertEqual(expected, actual, msg=f"{long=}")


if __name__ == "__main__":
    unittest.main()
