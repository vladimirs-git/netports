"""Tests vlan.py"""

import dictdiffer  # type: ignore[import-untyped]
import pytest

from netports import vlan
from netports.exceptions import NetportsValueError

ALL = list(range(1, 4095))


@pytest.mark.parametrize("kwargs, exp_ivlan, exp_svlan", [
    # vlans
    ({}, [], ""),
    ({"items": ""}, [], ""),
    ({"items": []}, [], ""),
    ({"items": 1}, [1], "1"),
    ({"items": "1"}, [1], "1"),
    ({"items": [1]}, [1], "1"),
    ({"items": ["1"]}, [1], "1"),
    ({"items": [4094]}, [4094], "4094"),
    ({"items": [5, 5, 1, 3, 4]}, [1, 3, 4, 5], "1,3-5"),
    ({"items": "3-5,1,3-5,1"}, [1, 3, 4, 5], "1,3-5"),
    # 1-4094
    ({"items": "1-4094"}, [-1], "1-4094"),
    ({"items": ALL}, [-1], "1-4094"),
    ({"items": ALL, "verbose": False}, [-1], "1-4094"),
    ({"items": ALL, "verbose": True}, ALL, "1-4094"),
    ({"items": "1-4094,1"}, [-1], "1-4094"),
    ({"items": [*ALL, 1]}, [-1], "1-4094"),
    # -1
    ({"items": -1}, [-1], "1-4094"),
    ({"items": "-1"}, [-1], "1-4094"),
    ({"items": [-1]}, [-1], "1-4094"),
    ({"items": ["-1"]}, [-1], "1-4094"),
    ({"items": [-1, 2]}, [-1], "1-4094"),
    ({"items": ["-1", "2"]}, [-1], "1-4094"),
    ({"items": [-1], "verbose": False}, [-1], "1-4094"),
    # all
    ({"all": True}, [-1], "1-4094"),
    ({"all": True, "verbose": False}, [-1], "1-4094"),
    ({"all": True, "verbose": True}, ALL, "1-4094"),
    ({"items": "1", "all": True}, [-1], "1-4094"),
    ({"items": "1", "all": True, "verbose": False}, [-1], "1-4094"),
    ({"items": "1", "all": True, "verbose": True}, ALL, "1-4094"),
    # splitter
    ({"items": "1,3-5", "platform": "cisco"}, [1, 3, 4, 5], "1,3-5"),
    ({"items": "1 3 to 5", "platform": "hpe"}, [1, 3, 4, 5], "1 3 to 5"),
    ({"items": "1,3-5", "splitter": ",", "range_splitter": "-"}, [1, 3, 4, 5], "1,3-5"),
    ({"items": "1 3 to 5", "splitter": " ", "range_splitter": " to "}, [1, 3, 4, 5], "1 3 to 5"),
    # splitter -1
    ({"items": "-1", "platform": "cisco"}, [-1], "1-4094"),
    ({"items": "-1", "platform": "hpe"}, [-1], "1 to 4094"),
    ({"items": "-1", "splitter": ",", "range_splitter": "-"}, [-1], "1-4094"),
    ({"items": "-1", "splitter": " ", "range_splitter": " to "}, [-1], "1 to 4094"),
    # invalid
    # vlans
    ({"items": 0}, NetportsValueError, NetportsValueError),
    ({"items": "0"}, NetportsValueError, NetportsValueError),
    ({"items": [0]}, NetportsValueError, NetportsValueError),
    ({"items": 4095}, NetportsValueError, NetportsValueError),
    ({"items": "4095"}, NetportsValueError, NetportsValueError),
    ({"items": [4095]}, NetportsValueError, NetportsValueError),
    # typo
    ({"items": "typo"}, ValueError, ValueError),
    # splitter
    ({"items": "1,3-5", "platform": "hpe"}, NetportsValueError, NetportsValueError),
    ({"items": "1 3 to 5", "platform": "cisco"}, NetportsValueError, NetportsValueError),
    # splitter -1 verbose
    ({"items": "-1", "verbose": True, "platform": "cisco"}, NetportsValueError, NetportsValueError),
    ({"items": "-1", "verbose": True, "platform": "hpe"}, NetportsValueError, NetportsValueError),
    ({"items": "-1", "verbose": True, "splitter": ",", "range_splitter": "-"},
     NetportsValueError, NetportsValueError),
    ({"items": "-1", "verbose": True, "splitter": " ", "range_splitter": " to "},
     NetportsValueError, NetportsValueError),
])
def test_valid__ivlan__svlan(kwargs, exp_ivlan, exp_svlan):
    """vlan.ivlan() vlan.svlan()."""
    if isinstance(exp_ivlan, list):
        act_ivlan = vlan.ivlan(**kwargs)
        act_svlan = vlan.svlan(**kwargs)

        assert act_ivlan == exp_ivlan
        assert act_svlan == exp_svlan
    else:
        with pytest.raises(exp_ivlan):
            vlan.ivlan(**kwargs)
        with pytest.raises(exp_svlan):
            vlan.svlan(**kwargs)


@pytest.mark.parametrize("item, kwargs, expected", [
    ("", {}, ""),
    ("1-3", {}, "1-3"),
    ("1-3", {"range_splitter": " to "}, "1 to 3"),
    ("1-3", {"splitter": " to "}, "1-3"),
])
def test_valid__replace_range_splitter(item, kwargs, expected):
    """vlan._replace_range_splitter()"""
    actual = vlan._replace_range_splitter(item=item, **kwargs)
    assert actual == expected


@pytest.mark.parametrize("kwargs, expected", [
    ({}, {}),
    ({"splitter": "a", "range_splitter": "a"}, dict(splitter="a", range_splitter="a")),
    ({"platform": "cisco"}, dict(platform="cisco", splitter=",", range_splitter="-")),
    ({"platform": "cisco", "splitter": "a", "range_splitter": "a"},
     {"platform": "cisco", "splitter": ",", "range_splitter": "-"}),
    ({"platform": "hpe", "splitter": "a", "range_splitter": "a"},
     {"platform": "hpe", "splitter": " ", "range_splitter": " to "}),
])
def test_valid__update_splitters(kwargs, expected):
    """vlan._update_splitters()"""
    result = vlan._update_splitters(**kwargs)

    diff = list(dictdiffer.diff(result, expected))
    assert diff == []
