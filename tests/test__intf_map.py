"""Tests intf_map.py"""

import difflib

import dictdiffer  # type: ignore[import-untyped]
import pytest

from netports import intf_map
from tests import params__intf_map as p


@pytest.mark.parametrize("kwargs, expected", [
    ({"device_type": "cisco_ios"}, p.LONGS_IOS),
    ({"device_type": "cisco_ios", "value_lower": True}, p.LONGS_IOS_LOWER_TRUE),
    ({"device_type": "cisco_ios", "value_lower": False}, p.LONGS_IOS_LOWER_FALE),
    ({}, p.LONGS),
])
def test__longs(kwargs, expected):
    """intf_map.longs()"""
    actual = intf_map.longs(**kwargs)

    diff = list(difflib.unified_diff(actual, expected, lineterm=""))
    diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
    assert diff == []


@pytest.mark.parametrize("kwargs, expected", [
    ({"value_lower": True}, p.SHORT_TO_LONG_VALUE_LOW),
    ({"key_lower": True}, p.SHORT_TO_LONG_KEY_LOW),
    ({"device_type": "cisco_ios"}, p.SHORT_TO_LONG_IOS),
    ({"device_type": "cisco_nxos"}, p.SHORT_TO_LONG_NXOS),
    ({"device_type": "cisco_xr"}, p.SHORT_TO_LONG_ASR),
    ({"device_type": "hp_comware"}, p.SHORT_TO_LONG_H3C),
    ({"device_type": "hp_procurve"}, p.SHORT_TO_LONG_HPC),
    ({}, p.SHORT_TO_LONG),
])
def test_valid__short_to_long(kwargs, expected):
    """intf_map.short_to_long()"""
    actual = intf_map.short_to_long(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert diff == []


@pytest.mark.parametrize("kwargs, expected", [
    ({"value_lower": True}, p.SHORT_TO_SHORT_VALUE_LOW),
    ({"key_lower": True}, p.SHORT_TO_SHORT_KEY_LOW),
    ({"device_type": "cisco_ios"}, p.SHORT_TO_SHORT_IOS),
    ({"device_type": "cisco_nxos"}, p.SHORT_TO_SHORT_NXOS),
    ({"device_type": "cisco_xr"}, p.SHORT_TO_SHORT_ASR),
    ({"device_type": "hp_comware"}, p.SHORT_TO_SHORT_H3C),
    ({"device_type": "hp_procurve"}, p.SHORT_TO_SHORT_HPC),
    ({}, p.SHORT_TO_SHORT),
])
def test_valid__short_to_short(kwargs, expected):
    """intf_map.short_to_short()"""
    actual = intf_map.short_to_short(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert diff == []


@pytest.mark.parametrize("kwargs, expected", [
    ({"value_lower": True}, p.LONG_TO_SHORT_VALUE_LOW),
    ({"key_lower": True}, p.LONG_TO_SHORT_KEY_LOW),
    ({"device_type": "cisco_ios"}, p.LONG_TO_SHORT_IOS),
    ({"device_type": "cisco_nxos"}, p.LONG_TO_SHORT_NXOS),
    ({"device_type": "cisco_xr"}, p.LONG_TO_SHORT_ASR),
    ({"device_type": "hp_comware"}, p.LONG_TO_SHORT_H3C),
    ({"device_type": "hp_procurve"}, p.LONG_TO_SHORT_HPC),
    ({}, p.LONG_TO_SHORT),
])
def test__long_to_short(kwargs, expected):
    """intf_map.long_to_short()"""
    actual = intf_map.long_to_short(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert diff == []


@pytest.mark.parametrize("kwargs, expected", [
    ({"value_lower": True}, p.LONG_TO_LONG_VALUE_LOW),
    ({"key_lower": True}, p.LONG_TO_LONG_KEY_LOW),
    ({"device_type": "cisco_ios"}, p.LONG_TO_LONG_IOS),
    ({"device_type": "cisco_nxos"}, p.LONG_TO_LONG_NXOS),
    ({"device_type": "cisco_xr"}, p.LONG_TO_LONG_ASR),
    ({"device_type": "hp_comware"}, p.LONG_TO_LONG_H3C),
    ({"device_type": "hp_procurve"}, p.LONG_TO_LONG_HPC),
    ({}, p.LONG_TO_LONG),
])
def test__long_to_long(kwargs, expected):
    """intf_map.long_to_long()"""
    actual = intf_map.long_to_long(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert diff == []


@pytest.mark.parametrize("kwargs, expected", [
    ({"device_type": "cisco_ios"}, p.SHORTS_IOS),
    ({"device_type": "cisco_ios", "value_lower": True}, p.SHORTS_IOS_LOWER_TRUE),
    ({"device_type": "cisco_ios", "value_lower": False}, p.SHORTS_IOS_LOWER_FALE),
    ({}, p.SHORTS),
])
def test__shorts(kwargs, expected):
    """intf_map.shorts()"""
    actual = intf_map.shorts(**kwargs)

    diff = list(difflib.unified_diff(actual, expected, lineterm=""))
    diff = [s for s in diff if s.startswith("-") or s.startswith("+")]
    assert diff == []
