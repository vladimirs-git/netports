"""Tests intf_gm.py"""

import random
from typing import Any

import pytest

from netports import intf_gm
from netports.intf import Intf
from netports.intf_gm import IntfGM

ETHERNET1 = "interface Ethernet1"
ETHERNET2 = "interface Ethernet2"
ETHERNET3 = "interface Ethernet3"
ETHERNET5 = "interface Ethernet5"
ETHERNET11 = "interface Ethernet11"
ETHERNET1_1 = "interface Ethernet1/2/3.1"
ETHERNET1_2 = "interface Ethernet1/2/3.2"
ETHERNET1_3 = "interface Ethernet1/2/3.3"
ETHERNET1_5 = "interface Ethernet1/2/3.5"
ETHERNET1_11 = "interface Ethernet1/2/3.11"


# =========================== property ===========================

@pytest.mark.parametrize("items, expected", [
    ("p1", ["p1"]),
    (["p3", "p1", "p2"], ["p1", "p2", "p3"]),
    (("p1", "p2"), ["p1", "p2"]),
    (Intf("p1"), ["p1"]),
    ([Intf("p3"), Intf("p1"), Intf("p2")], ["p1", "p2", "p3"]),
    (["3", "1", "2"], ["1", "2", "3"]),
    ([3, 1, 2], ["1", "2", "3"]),
    # empty
    (None, []),
    ("", []),
    ([], []),
])
def test__items(items, expected):
    """IntfGM.items"""
    if isinstance(items, list):
        random.shuffle(items)
    obj = IntfGM(items=items)

    actual = [str(o) for o in obj.items]
    assert actual == expected


# =========================== methods ===========================

@pytest.mark.parametrize("fmt, expected", [
    ("long", ["interface Ethernet1-3", "interface Ethernet1/2/3.1-3"]),
    ("short", ["Eth1-3", "Eth1/2/3.1-3"]),
])
def test__range(fmt, expected):
    """IntfGM.range()"""
    intfs = [ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET1_1, ETHERNET1_2, ETHERNET1_3]

    random.shuffle(intfs)
    obj = IntfGM(items=intfs)

    actual = obj.ranges(fmt=fmt)

    assert actual == expected


# =========================== helpers ============================

@pytest.mark.parametrize("items, expected", [
    (["p1"], ["p1"]),
    (["p1", "p2", "p3", "p5", "p6", "p7", "p9"], ["p1-3", "p5-7", "p9"]),
    ([1, 2, 3, 5, 6, 7, 9], ["1-3", "5-7", "9"]),
    (["p1/1", "p1/2", "p1/3", "p1/5", "p1/6", "p1/7", "p2/1", "p2/2", "p2/3", "p2/5"],
     ["p1/1-3", "p1/5-7", "p2/1-3", "p2/5"]),
    (["1", "2", "3", "1/1", "1/2", "1/3", "1/2.3", "1/2.4", "1/2.5"],
     ["1-3", "1/1-3", "1/2.3-5"]),
    ([], []),
])
def test__ranges__long(items, expected):
    """IntfGM._ranges__long()"""
    random.shuffle(items)
    obj = IntfGM(items)

    actual = obj._ranges__long()

    assert actual == expected


@pytest.mark.parametrize("items, expected", [
    ([ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET5], ["Eth1-3", "Eth5"]),
    ([ETHERNET1_1, ETHERNET1_2, ETHERNET1_3, ETHERNET1_5], ["Eth1/2/3.1-3", "Eth1/2/3.5"]),
    ([1, 2, 3, 5], ["1-3", "5"]),
])
def test__ranges__short(items, expected):
    """IntfGM._ranges__short()"""
    random.shuffle(items)
    obj = IntfGM(items=items)

    actual = obj._ranges__short()

    assert actual == expected


# ============================ functions =============================

# noinspection DuplicatedCode
@pytest.mark.parametrize("start, end, base, expected", [
    ("1", "3", "", ["1", "2", "3"]),
    (ETHERNET1, ETHERNET11, "", [f"interface Ethernet{i}" for i in range(1, 12)]),
    (ETHERNET1_1, ETHERNET1_11, "", [f"interface Ethernet1/2/3.{i}" for i in range(1, 12)]),
    # base
    ("1", "3", "interface ", ["interface 1", "interface 2", "interface 3"]),
])
def test__generate_intfs(start, end, base, expected):
    """intf_gm.generate_intfs()"""
    intfs = intf_gm.generate_intfs(start=start, end=end, base=base)

    actual = [o.line for o in intfs]
    assert actual == expected


# noinspection DuplicatedCode
@pytest.mark.parametrize("start, end, base, expected", [
    ("1", "3", "", ["1", "2", "3"]),
    (ETHERNET1, ETHERNET11, "", [f"interface Ethernet{i}" for i in range(1, 12)]),
    (ETHERNET1_1, ETHERNET1_11, "", [f"interface Ethernet1/2/3.{i}" for i in range(1, 12)]),
    # base
    ("1", "3", "interface ", ["interface 1", "interface 2", "interface 3"]),
])
def test__generate_names(start, end, base, expected):
    """intf_gm.generate_names()"""
    actual = intf_gm.generate_names(start=start, end=end, base=base)

    assert actual == expected


@pytest.mark.parametrize("items, fmt, expected", [
    # long
    ([ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET5], "long", f"{ETHERNET1}-3,{ETHERNET5}"),
    ([ETHERNET1_1, ETHERNET1_2, ETHERNET1_5], "long", f"{ETHERNET1_1}-2,{ETHERNET1_5}"),
    (["1/1", "1/2", "1/3", "1/5"], "long", "1/1-3,1/5"),
    ([1, 2, 3, 5], "long", "1-3,5"),
    # short
    ([ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET5], "short", "Eth1-3,Eth5"),
    ([ETHERNET1_1, ETHERNET1_2, ETHERNET1_5], "short", "Eth1/2/3.1-2,Eth1/2/3.5"),
    (["1/1", "1/2", "1/3", "1/5"], "short", "1/1-3,1/5"),
    ([1, 2, 3, 5], "short", "1-3,5"),
])
def test__names_to_range(items, fmt, expected):
    """intf_gm.names_to_range()"""
    random.shuffle(items)

    actual = intf_gm.names_to_range(names=items, fmt=fmt)

    assert actual == expected


# noinspection DuplicatedCode
@pytest.mark.parametrize("line, base, expected", [
    ("p1", "", ["p1"]),  # single
    ("p1,p1", "", ["p1"]),  # remove duplicate
    ("Eth1/1-3,Eth1/5", "", ["Eth1/1", "Eth1/2", "Eth1/3", "Eth1/5"]),
    (f"{ETHERNET1}-3,{ETHERNET5}", "", [ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET5]),
    (f"{ETHERNET1_1}-2,{ETHERNET1_5}", "", [ETHERNET1_1, ETHERNET1_2, ETHERNET1_5]),
    ("1/1-3,1/5", "", ["1/1", "1/2", "1/3", "1/5"]),
    ("1-3,5", "", ["1", "2", "3", "5"]),
    ("p1-3,Eth1-3,1-3", "", ["1", "2", "3", "Eth1", "Eth2", "Eth3", "p1", "p2", "p3"]),  # combo
    # base
    ("1/1-3,1/5", "Eth", ["Eth1/1", "Eth1/2", "Eth1/3", "Eth1/5"]),
    # ("1-3,5", "interface ", ["interface 1", "interface 2", "interface 3", "interface 5"]),
])
def test__range_to_intfs(line, base, expected):
    """intf_gm.range_to_intfs()"""
    intfs = intf_gm.range_to_intfs(line=line, base=base)

    actual = [o.line for o in intfs]
    assert actual == expected


@pytest.mark.parametrize("line, base, expected", [
    ("p1", "", ["p1"]),  # single
    ("p1,p1", "", ["p1"]),  # duplicate
    ("47-48", "", ["47", "48"]),  # long digit without base
    ("p11/1-11", "", [f"p11/{i}" for i in range(1, 12)]),  # long digit
    (f"{ETHERNET1}-3,{ETHERNET5}", "", [ETHERNET1, ETHERNET2, ETHERNET3, ETHERNET5]),
    (f"{ETHERNET1_1}-2,{ETHERNET1_5}", "", [ETHERNET1_1, ETHERNET1_2, ETHERNET1_5]),
    ("1/1-3,1/5", "", ["1/1", "1/2", "1/3", "1/5"]),
    ("1-3,5", "", ["1", "2", "3", "5"]),
    ("p1-3,Eth1-3,1-3", "", ["1", "2", "3", "Eth1", "Eth2", "Eth3", "p1", "p2", "p3"]),  # combo
    ("2/47-2/48", "", ["2/47", "2/48"]),  # hp_procurve, trunk 2/47-2/48 trk2
    # base
    ("1-3,5", "interface ", ["interface 1", "interface 2", "interface 3", "interface 5"]),
    # invalid
    ("-", "", ValueError),
    ("1-2-3", "", ValueError),
    ("1-a", "", ValueError),
    ("a-2", "", ValueError),
])
def test__range_to_names(line, base, expected: Any):
    """intf_gm.range_to_names()"""
    if isinstance(expected, list):
        actual = intf_gm.range_to_names(line=line, base=base)
        assert actual == expected
    else:
        with pytest.raises(expected):
            intf_gm.range_to_names(line=line, base=base)
