"""Unittest sw_version.py"""

import pytest

from netports.swversion import SwVersion
from tests import params__swversion as p


@pytest.mark.parametrize("text, expected", [
    ("", p.V0),
    ("0", p.V0),
    (0, p.V0),
    ("1", p.V1),
    (1, p.V1),
    ("1.2", p.V2),
    ("1.2.3", p.V3),
    ("11.22.33.44", p.V4),
    ("11.22.33.44.55", p.V5),
    # cisco
    ("11.22(33)SE", p.CISCO1),
    ("11.22(33)SE44", p.CISCO2),
])
def test__init__(text, expected):
    """SwVersion.__init__()"""
    obj = SwVersion(text)
    for attr, expected_ in expected.items():
        actual = getattr(obj, attr)
        assert actual == expected_


@pytest.mark.parametrize("text1, text2, expected", [
    # cisco_ios
    ("11.22(33)SE44", "11.22(33)SE44", True),
    ("1.22(33)SE44", "11.22(33)SE44", False),
    ("11.22(3)SE44", "11.22(33)SE44", False),
    ("11.22(33)SE4", "11.22(33)SE44", False),
    ("11.22(33)XX44", "11.22(33)SE44", False),
    ("11.22(33)", "11.22(33)SE44", False),
    # hp_procurve
    ("YA.11.22.0033", "YA.11.22.0033", True),
    ("YA.11.22.0033", "YA.11.22.0034", False),
    # combo
    ("11.22(33)", "YA.11.22.33", False),
])
def test__eq__(text1, text2, expected):
    """SwVersion.__eq__()"""
    obj1 = SwVersion(text1)
    obj2 = SwVersion(text2)
    actual = bool(obj1 == obj2)
    assert actual == expected


@pytest.mark.parametrize("text1, text2, expected", [
    ("2.2(2)A2", "2.2(2)A2", True),
    ("2.2(2)A2", "2.2(2)B2", True),
    ("2.2(2)A2", "1.2(2)A2", False),
    ("2.2(2)A2", "3.2(2)A2", True),
    ("2.2(2)A2", "2.1(2)A2", False),
    ("2.2(2)A2", "2.3(2)A2", True),
    ("2.2(2)A2", "2.2(1)A2", False),
    ("2.2(2)A2", "2.2(3)A2", True),
    ("2.2(2)A2", "2.2(2)A1", False),
    ("2.2(2)A2", "2.2(2)A3", True),
])
def test__le__(text1, text2, expected):
    """SwVersion.__le__()"""
    obj1 = SwVersion(text1)
    obj2 = SwVersion(text2)
    actual = bool(obj1 <= obj2)
    assert actual == expected
