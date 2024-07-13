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
            # value_lower=None
            (dict(), 'ABBEEFFFGHLMMMMPSTTTTTTVVVabbeefffghlmmmmmpstttttttvvv'),
            (dict(device_type="cisco_asr"), 'ABEEFFFGHLMMMMPSTTTVVVabeefffghlmmmmpsttttvvv'),
            (dict(device_type="cisco_ios"), 'AEEFFFGHLMMMPSTTTTVVVaeefffghlmmmpsttttvvv'),
            (dict(device_type="cisco_nxos"), 'AEEFFFGHMMMSTTTTVVVaeefffghlmmmmpsttttvvv'),
            (dict(device_type="hp_comware"), 'ABEEFFFGHLMMMPSTTTTVVVVabeefffghlmmmpsttttvvvv'),
            (dict(device_type="hp_procurve"), 'AEEFFFGHLMMMPSTTTTTVVVaeefffghlmmmpstttttvvv'),
            # value_lower=True
            (dict(value_lower=True), 'abbeefffghlmmmmmpstttttttvvv'),
            (dict(device_type="cisco_asr", value_lower=True), 'abeefffghlmmmmpsttttvvv'),
            (dict(device_type="cisco_ios", value_lower=True), 'aeefffghlmmmpsttttvvv'),
            (dict(device_type="cisco_nxos", value_lower=True), 'aeefffghlmmmmpsttttvvv'),
            (dict(device_type="hp_comware", value_lower=True), 'abeefffghlmmmpsttttvvvv'),
            (dict(device_type="hp_procurve", value_lower=True), 'aeefffghlmmmpstttttvvv'),
            # value_lower=False
            (dict(value_lower=False), 'ABBEEFFFGHLMMMMPSTTTTTTVVVmt'),
            (dict(device_type="cisco_asr", value_lower=False), 'ABEEFFFGHLMMMMPSTTTVVVt'),
            (dict(device_type="cisco_ios", value_lower=False), 'AEEFFFGHLMMMPSTTTTVVV'),
            (dict(device_type="cisco_nxos", value_lower=False), 'AEEFFFGHMMMSTTTTVVVlmp'),
            (dict(device_type="hp_comware", value_lower=False), 'ABEEFFFGHLMMMPSTTTTVVVV'),
            (dict(device_type="hp_procurve", value_lower=False), 'AEEFFFGHLMMMPSTTTTTVVV'),
        ]:
            results = intf_map.longs(**kwargs)
            actual = "".join([s[0] for s in results])
            assert actual == expected

    def test_valid__short_to_long(self):
        """intf_map.short_to_long()"""
        for kwargs, expected in [
            (dict(), hm.SHORT_TO_LONG),
            (dict(value_lower=True), hm.SHORT_TO_LONG_VALUE_LOW),
            (dict(key_lower=True), hm.SHORT_TO_LONG_KEY_LOW),
            (dict(device_type="cisco_asr"), hm.SHORT_TO_LONG_ASR),
            (dict(device_type="cisco_ios"), hm.SHORT_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), hm.SHORT_TO_LONG_NXOS),
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
            (dict(device_type="cisco_asr"), hm.SHORT_TO_SHORT_ASR),
            (dict(device_type="cisco_ios"), hm.SHORT_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), hm.SHORT_TO_SHORT_NXOS),
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
            (dict(device_type="cisco_asr"), hm.LONG_TO_SHORT_ASR),
            (dict(device_type="cisco_ios"), hm.LONG_TO_SHORT_IOS),
            (dict(device_type="cisco_nxos"), hm.LONG_TO_SHORT_NXOS),
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
            (dict(device_type="cisco_asr"), hm.LONG_TO_LONG_ASR),
            (dict(device_type="cisco_ios"), hm.LONG_TO_LONG_IOS),
            (dict(device_type="cisco_nxos"), hm.LONG_TO_LONG_NXOS),
            (dict(device_type="hp_comware"), hm.LONG_TO_LONG_H3C),
            (dict(device_type="hp_procurve"), hm.LONG_TO_LONG_HPC),
        ]:
            actual = intf_map.long_to_long(**kwargs)
            diff = list(dictdiffer.diff(actual, expected))
            self.assertEqual(diff, [], msg=f"{kwargs=}")

    def test_valid__shorts(self):
        """intf_map.shorts()"""
        for kwargs, expected in [
            # value_lower=None
            (dict(), 'ABBEEFFFGGHLMMMMPSTTTTTVVVVXabbeefffgghlmmmmmpsttttttvvvvx'),
            (dict(device_type="cisco_asr"), 'ABEEFFFGHLMMMMPSTTTTVVVVabeefffghlmmmmpstttttvvvv'),
            (dict(device_type="cisco_ios"), 'AEEFFFGHLMMMPSTTTTVVVVaeefffghlmmmpsttttvvvv'),
            (dict(device_type="cisco_nxos"), 'AEEFFFGHLMMMPSTTTTVVVVaeefffghlmmmmpsttttvvvv'),
            (dict(device_type="hp_comware"), 'ABEEFFFGGHLMMMPSTTTTVVVVXabeefffgghlmmmpsttttvvvvx'),
            (dict(device_type="hp_procurve"), 'AEEFFFGHLMMMPSTTTTTVVVVaeefffghlmmmpstttttvvvv'),
            # value_lower=True
            (dict(value_lower=True), 'abbeefffgghlmmmmmpsttttttvvvvx'),
            (dict(device_type="cisco_asr", value_lower=True), 'abeefffghlmmmmpstttttvvvv'),
            (dict(device_type="cisco_ios", value_lower=True), 'aeefffghlmmmpsttttvvvv'),
            (dict(device_type="cisco_nxos", value_lower=True), 'aeefffghlmmmmpsttttvvvv'),
            (dict(device_type="hp_comware", value_lower=True), 'abeefffgghlmmmpsttttvvvvx'),
            (dict(device_type="hp_procurve", value_lower=True), 'aeefffghlmmmpstttttvvvv'),
            # value_lower=False
            (dict(value_lower=False), 'ABBEEFFFGGHLMMMMPSTTTTTVVVVXmt'),
            (dict(device_type="cisco_asr", value_lower=False), 'ABEEFFFGHLMMMMPSTTTTVVVVt'),
            (dict(device_type="cisco_ios", value_lower=False), 'AEEFFFGHLMMMPSTTTTVVVV'),
            (dict(device_type="cisco_nxos", value_lower=False), 'AEEFFFGHLMMMPSTTTTVVVVm'),
            (dict(device_type="hp_comware", value_lower=False), 'ABEEFFFGGHLMMMPSTTTTVVVVX'),
            (dict(device_type="hp_procurve", value_lower=False), 'AEEFFFGHLMMMPSTTTTTVVVV'),
        ]:
            results = intf_map.shorts(**kwargs)
            actual = "".join([s[0] for s in results])
            assert actual == expected


if __name__ == "__main__":
    unittest.main()
