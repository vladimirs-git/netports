"""Tests tcp.py"""

import pytest

from netports import tcp, NetportsValueError

ALL = list(range(1, 65536))


@pytest.mark.parametrize("kwargs, exp_itcp, exp_stcp", [
    # ports
    ({}, [], ""),
    ({"items": ""}, [], ""),
    ({"items": []}, [], ""),
    ({"items": 1}, [1], "1"),
    ({"items": "1"}, [1], "1"),
    ({"items": [1]}, [1], "1"),
    ({"items": ["1"]}, [1], "1"),
    ({"items": [65535]}, [65535], "65535"),
    ({"items": [5, 5, 1, 3, 4]}, [1, 3, 4, 5], "1,3-5"),
    ({"items": "3-5,1,3-5,1"}, [1, 3, 4, 5], "1,3-5"),
    # 1-65535
    ({"items": "1-65535"}, [-1], "1-65535"),
    ({"items": ALL}, [-1], "1-65535"),
    ({"items": ALL, "verbose": False}, [-1], "1-65535"),
    ({"items": ALL, "verbose": True}, ALL, "1-65535"),
    ({"items": "1-65535,1"}, [-1], "1-65535"),
    ({"items": [*ALL, 1]}, [-1], "1-65535"),
    # -1
    ({"items": -1}, [-1], "1-65535"),
    ({"items": "-1"}, [-1], "1-65535"),
    ({"items": [-1]}, [-1], "1-65535"),
    ({"items": ["-1"]}, [-1], "1-65535"),
    ({"items": [-1, 2]}, [-1], "1-65535"),
    ({"items": ["-1", "2"]}, [-1], "1-65535"),
    ({"items": [-1], "verbose": False}, [-1], "1-65535"),
    # all
    ({"all": True}, [-1], "1-65535"),
    ({"all": True, "verbose": False}, [-1], "1-65535"),
    ({"all": True, "verbose": True}, ALL, "1-65535"),
    ({"items": "1", "all": True}, [-1], "1-65535"),
    ({"items": "1", "all": True, "verbose": False}, [-1], "1-65535"),
    ({"items": "1", "all": True, "verbose": True}, ALL, "1-65535"),
    # ports
    ({"items": 0}, NetportsValueError, NetportsValueError),
    ({"items": "0"}, NetportsValueError, NetportsValueError),
    ({"items": [0]}, NetportsValueError, NetportsValueError),
    ({"items": 65536}, NetportsValueError, NetportsValueError),
    ({"items": "65536"}, NetportsValueError, NetportsValueError),
    ({"items": [65536]}, NetportsValueError, NetportsValueError),
    # typo
    ({"items": "typo"}, ValueError, ValueError),
])
def test_valid__itcp__stcp(kwargs, exp_itcp, exp_stcp):
    """tcp.itcp() tcp.stcp()"""
    if isinstance(exp_itcp, list):
        act_itcp = tcp.itcp(**kwargs)
        act_stcp = tcp.stcp(**kwargs)

        assert act_itcp == exp_itcp
        assert act_stcp == exp_stcp
    else:
        with pytest.raises(exp_itcp):
            tcp.itcp(**kwargs)
        with pytest.raises(exp_stcp):
            tcp.stcp(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({"port": "", "strict": True}, TypeError),
    ({"port": "", "strict": False}, TypeError),
    ({"port": {}, "strict": True}, TypeError),
    ({"port": {}, "strict": False}, TypeError),
    ({"port": "-1", "strict": True}, TypeError),
    ({"port": "-1", "strict": False}, TypeError),
    ({"port": -1, "strict": True}, NetportsValueError),
    ({"port": -1, "strict": False}, False),
    ({"port": "0", "strict": True}, TypeError),
    ({"port": "0", "strict": False}, TypeError),
    ({"port": 0, "strict": True}, NetportsValueError),
    ({"port": 0, "strict": False}, False),
    ({"port": "1", "strict": True}, TypeError),
    ({"port": "1", "strict": False}, TypeError),
    ({"port": 1, "strict": True}, True),
    ({"port": 1, "strict": False}, True),
    ({"port": "65535", "strict": True}, TypeError),
    ({"port": "65535", "strict": False}, TypeError),
    ({"port": 65535, "strict": True}, True),
    ({"port": 65535, "strict": False}, True),
    ({"port": "65536", "strict": True}, TypeError),
    ({"port": "65536", "strict": False}, TypeError),
    ({"port": 65536, "strict": True}, NetportsValueError),
    ({"port": 65536, "strict": False}, False),
])
def test__check_port(kwargs, expected):
    """tcp.check_port()"""
    if isinstance(expected, bool):
        actual = tcp.check_port(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            tcp.check_port(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    ({"ports": [], "strict": True}, True),
    ({"ports": [], "strict": False}, True),
    ({"ports": ["1"], "strict": True}, TypeError),
    ({"ports": ["1"], "strict": False}, TypeError),
    ({"ports": [1, 65535], "strict": True}, True),
    ({"ports": [1, 65535], "strict": False}, True),
    ({"ports": ["0"], "strict": True}, TypeError),
    ({"ports": ["0"], "strict": False}, TypeError),
])
def test__check_ports(kwargs, expected):
    """check_ports()"""
    if isinstance(expected, bool):
        actual = tcp.check_ports(**kwargs)
        assert actual == expected
    else:
        with pytest.raises(expected):
            tcp.check_port(**kwargs)
