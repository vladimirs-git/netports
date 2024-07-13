"""unittest intf_map.py"""

import unittest

import dictdiffer  # type: ignore

from netports import intf_map
from tests import helpers__intf_map as hm


# noinspection DuplicatedCode
class Test(unittest.TestCase):
    """unittest intf_map.py"""

    def test_valid__longs(self):
        """intf_map.longs()"""
        for kwargs, expected in [
            (dict(), hm.LONGS),
            (dict(device_type="cisco_ios"), hm.LONGS_IOS),
            (dict(device_type="cisco_ios", value_lower=True), hm.LONGS_IOS_LOWER_TRUE),
            (dict(device_type="cisco_ios", value_lower=False), hm.LONGS_IOS_LOWER_FALE),
        ]:
            actual = intf_map.longs(**kwargs)
            assert actual == expected

    def test_valid__short_to_long(self):
        """intf_map.short_to_long()"""
        for kwargs, expected in [
            (dict(), hm.SHORT_TO_LONG),
            (dict(value_lower=True), hm.SHORT_TO_LONG_VALUE_LOW),
            (dict(key_lower=True), hm.SHORT_TO_LONG_KEY_LOW),
            (dict(device_type="cisco_ios"), hm.SHORT_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), hm.SHORT_TO_LONG_NXOS),
            (dict(device_type="cisco_xr"), hm.SHORT_TO_LONG_ASR),
            (dict(device_type="hp_comware"), hm.SHORT_TO_LONG_H3C),
            (dict(device_type="hp_procurve"), hm.SHORT_TO_LONG_HPC),
        ]:
            actual = intf_map.short_to_long(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__short_to_short(self):
        """intf_map.short_to_short()"""
        for kwargs, expected in [
            (dict(), hm.SHORT_TO_SHORT),
            (dict(value_lower=True), hm.SHORT_TO_SHORT_VALUE_LOW),
            (dict(key_lower=True), hm.SHORT_TO_SHORT_KEY_LOW),
            (dict(device_type="cisco_ios"), hm.SHORT_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), hm.SHORT_TO_SHORT_NXOS),
            (dict(device_type="cisco_xr"), hm.SHORT_TO_SHORT_ASR),
            (dict(device_type="hp_comware"), hm.SHORT_TO_SHORT_H3C),
            (dict(device_type="hp_procurve"), hm.SHORT_TO_SHORT_HPC),
        ]:
            actual = intf_map.short_to_short(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__long_to_short(self):
        """intf_map.long_to_short()"""
        for kwargs, expected in [
            (dict(), hm.LONG_TO_SHORT),
            (dict(value_lower=True), hm.LONG_TO_SHORT_VALUE_LOW),
            (dict(key_lower=True), hm.LONG_TO_SHORT_KEY_LOW),
            (dict(device_type="cisco_ios"), hm.LONG_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), hm.LONG_TO_SHORT_NXOS),
            (dict(device_type="cisco_xr"), hm.LONG_TO_SHORT_ASR),
            (dict(device_type="hp_comware"), hm.LONG_TO_SHORT_H3C),
            (dict(device_type="hp_procurve"), hm.LONG_TO_SHORT_HPC),
        ]:
            actual = intf_map.long_to_short(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__long_to_long(self):
        """intf_map.long_to_long()"""
        for kwargs, expected in [
            (dict(), hm.LONG_TO_LONG),
            (dict(value_lower=True), hm.LONG_TO_LONG_VALUE_LOW),
            (dict(key_lower=True), hm.LONG_TO_LONG_KEY_LOW),
            (dict(device_type="cisco_ios"), hm.LONG_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), hm.LONG_TO_LONG_NXOS),
            (dict(device_type="cisco_xr"), hm.LONG_TO_LONG_ASR),
            (dict(device_type="hp_comware"), hm.LONG_TO_LONG_H3C),
            (dict(device_type="hp_procurve"), hm.LONG_TO_LONG_HPC),
        ]:
            actual = intf_map.long_to_long(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__shorts(self):
        """intf_map.shorts()"""
        for kwargs, expected in [
            (dict(), hm.SHORTS),
            (dict(device_type="cisco_ios"), hm.SHORTS_IOS),
            (dict(device_type="cisco_ios", value_lower=True), hm.SHORTS_IOS_LOWER_TRUE),
            (dict(device_type="cisco_ios", value_lower=False), hm.SHORTS_IOS_LOWER_FALE),
        ]:
            actual = intf_map.shorts(**kwargs)
            x = 1
            # assert actual == expected


if __name__ == "__main__":
    unittest.main()
