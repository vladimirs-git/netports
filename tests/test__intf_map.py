"""Tests intf_map.py"""

import difflib
import unittest

import dictdiffer  # type: ignore[import-untyped]

from netports import intf_map
from tests import params__intf_map as p


# noinspection DuplicatedCode
class Test(unittest.TestCase):
    """Tests intf_map.py"""

    def test_valid__longs(self):
        """intf_map.longs()"""
        for kwargs, expected in [
            (dict(), p.LONGS),
            (dict(device_type="cisco_ios"), p.LONGS_IOS),
            (dict(device_type="cisco_ios", value_lower=True), p.LONGS_IOS_LOWER_TRUE),
            (dict(device_type="cisco_ios", value_lower=False), p.LONGS_IOS_LOWER_FALE),
        ]:
            actual = intf_map.longs(**kwargs)
            diff = list(difflib.unified_diff(actual, expected, lineterm=""))
            diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__short_to_long(self):
        """intf_map.short_to_long()"""
        for kwargs, expected in [
            (dict(), p.SHORT_TO_LONG),
            (dict(value_lower=True), p.SHORT_TO_LONG_VALUE_LOW),
            (dict(key_lower=True), p.SHORT_TO_LONG_KEY_LOW),
            (dict(device_type="cisco_ios"), p.SHORT_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), p.SHORT_TO_LONG_NXOS),
            (dict(device_type="cisco_xr"), p.SHORT_TO_LONG_ASR),
            (dict(device_type="hp_comware"), p.SHORT_TO_LONG_H3C),
            (dict(device_type="hp_procurve"), p.SHORT_TO_LONG_HPC),
        ]:
            actual = intf_map.short_to_long(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__short_to_short(self):
        """intf_map.short_to_short()"""
        for kwargs, expected in [
            (dict(), p.SHORT_TO_SHORT),
            (dict(value_lower=True), p.SHORT_TO_SHORT_VALUE_LOW),
            (dict(key_lower=True), p.SHORT_TO_SHORT_KEY_LOW),
            (dict(device_type="cisco_ios"), p.SHORT_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), p.SHORT_TO_SHORT_NXOS),
            (dict(device_type="cisco_xr"), p.SHORT_TO_SHORT_ASR),
            (dict(device_type="hp_comware"), p.SHORT_TO_SHORT_H3C),
            (dict(device_type="hp_procurve"), p.SHORT_TO_SHORT_HPC),
        ]:
            actual = intf_map.short_to_short(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__long_to_short(self):
        """intf_map.long_to_short()"""
        for kwargs, expected in [
            (dict(), p.LONG_TO_SHORT),
            (dict(value_lower=True), p.LONG_TO_SHORT_VALUE_LOW),
            (dict(key_lower=True), p.LONG_TO_SHORT_KEY_LOW),
            (dict(device_type="cisco_ios"), p.LONG_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), p.LONG_TO_SHORT_NXOS),
            (dict(device_type="cisco_xr"), p.LONG_TO_SHORT_ASR),
            (dict(device_type="hp_comware"), p.LONG_TO_SHORT_H3C),
            (dict(device_type="hp_procurve"), p.LONG_TO_SHORT_HPC),
        ]:
            actual = intf_map.long_to_short(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__long_to_long(self):
        """intf_map.long_to_long()"""
        for kwargs, expected in [
            (dict(), p.LONG_TO_LONG),
            (dict(value_lower=True), p.LONG_TO_LONG_VALUE_LOW),
            (dict(key_lower=True), p.LONG_TO_LONG_KEY_LOW),
            (dict(device_type="cisco_ios"), p.LONG_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), p.LONG_TO_LONG_NXOS),
            (dict(device_type="cisco_xr"), p.LONG_TO_LONG_ASR),
            (dict(device_type="hp_comware"), p.LONG_TO_LONG_H3C),
            (dict(device_type="hp_procurve"), p.LONG_TO_LONG_HPC),
        ]:
            actual = intf_map.long_to_long(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__shorts(self):
        """intf_map.shorts()"""
        for kwargs, expected in [
            (dict(), p.SHORTS),
            (dict(device_type="cisco_ios"), p.SHORTS_IOS),
            (dict(device_type="cisco_ios", value_lower=True), p.SHORTS_IOS_LOWER_TRUE),
            (dict(device_type="cisco_ios", value_lower=False), p.SHORTS_IOS_LOWER_FALE),
        ]:
            actual = intf_map.shorts(**kwargs)
            diff = list(difflib.unified_diff(actual, expected, lineterm=""))
            diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
            self.assertEqual(diff, [], msg=f"{kwargs=}")


if __name__ == "__main__":
    unittest.main()
