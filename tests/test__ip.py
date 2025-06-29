"""Tests ip.py"""

import dictdiffer  # type: ignore[import-untyped]
import pytest

from netports import ip, NetportsValueError

ALL = list(range(0, 256))


@pytest.mark.parametrize("kwargs, exp_iip, exp_sip", [
    # ports
    ({}, [], ""),
    ({"items": ""}, [], ""),
    ({"items": []}, [], ""),
    ({"items": 0}, [0], "0"),
    ({"items": "0"}, [0], "0"),
    ({"items": [0]}, [0], "0"),
    ({"items": 255}, [255], "255"),
    ({"items": [5, 5, 0, 3, 4]}, [0, 3, 4, 5], "0,3-5"),
    ({"items": "3-5,0,3-4,0"}, [0, 3, 4, 5], "0,3-5"),
    ({"items": "1,256", "strict": False}, [1], "1"),
    # name
    ({"items": "icmp"}, [1], "1"),
    ({"items": ["icmp"]}, [1], "1"),
    ({"items": "icmp,tcp"}, [1, 6], "1,6"),
    ({"items": ["icmp", "tcp"]}, [1, 6], "1,6"),
    ({"items": "icmp,1,icmp,1,5,3-4,tcp"}, [1, 3, 4, 5, 6], "1,3-6"),
    ({"items": "icmp,typo", "strict": False}, [1], "1"),
    # 0-255
    ({"items": "0-255"}, [-1], "0-255"),
    ({"items": ALL}, [-1], "0-255"),
    ({"items": ALL, "verbose": False}, [-1], "0-255"),
    ({"items": ALL, "verbose": True}, ALL, "0-255"),
    ({"items": "0-255,1"}, [-1], "0-255"),
    ({"items": [*ALL, 1]}, [-1], "0-255"),
    ({"items": "0-255,icmp"}, [-1], "0-255"),
    ({"items": [*ALL, "icmp"]}, [-1], "0-255"),
    ({"items": [*ALL, 256, "typo"], "strict": False}, [-1], "0-255"),
    # -1
    ({"items": -1}, [-1], "0-255"),
    ({"items": "-1"}, [-1], "0-255"),
    ({"items": [-1]}, [-1], "0-255"),
    ({"items": ["-1"]}, [-1], "0-255"),
    ({"items": [-1, 2]}, [-1], "0-255"),
    ({"items": ["-1", "2"]}, [-1], "0-255"),
    ({"items": [-1], "verbose": False}, [-1], "0-255"),
    ({"items": ["-1", 256, "typo"], "strict": False}, [-1], "0-255"),
    # all
    ({"all": True}, [-1], "0-255"),
    ({"all": True, "verbose": False}, [-1], "0-255"),
    ({"all": True, "verbose": True}, ALL, "0-255"),
    ({"items": "1", "all": True}, [-1], "0-255"),
    ({"items": "1", "all": True, "verbose": False}, [-1], "0-255"),
    ({"items": "1", "all": True, "verbose": True}, ALL, "0-255"),
    # combo
    ({"items": "1,ipinip,255"}, [1, 4, 255], "1,4,255"),
    ({"items": "1,ipinip,255,256,typo", "strict": False}, [1, 4, 255], "1,4,255"),
    # ports
    ({"items": 256}, NetportsValueError, NetportsValueError),
    ({"items": "256"}, NetportsValueError, NetportsValueError),
    ({"items": [256]}, NetportsValueError, NetportsValueError),
    # typo
    ({"items": "typo"}, NetportsValueError, NetportsValueError),
])
def test__iip(kwargs, exp_iip, exp_sip):
    """ip.iip() ip.sip()"""
    if isinstance(exp_iip, list):
        act_iip = ip.iip(**kwargs)
        act_sip = ip.sip(**kwargs)

        assert act_iip == exp_iip
        assert act_sip == exp_sip
    else:
        with pytest.raises(exp_iip):
            ip.iip(**kwargs)
        with pytest.raises(exp_sip):
            ip.sip(**kwargs)


@pytest.mark.parametrize("kwargs, expected", [
    # ports
    ({"items": ""}, ([], [])),
    ({"items": []}, ([], [])),
    ({"items": "1"}, ([(1, "icmp")], [])),
    ({"items": 1}, ([(1, "icmp")], [])),
    ({"items": ["1"]}, ([(1, "icmp")], [])),
    ({"items": [1]}, ([(1, "icmp")], [])),
    ({"items": "255"}, ([(255, "")], [])),
    # name
    ({"items": "icmp"}, ([(1, "icmp")], [])),
    ({"items": ["icmp"]}, ([(1, "icmp")], [])),
    ({"items": "tcp,icmp"}, ([(1, "icmp"), (6, "tcp")], [])),
    ({"items": ["tcp", "icmp"]}, ([(1, "icmp"), (6, "tcp")], [])),
    # alias
    ({"items": "ipinip"}, ([(4, "ipinip")], [])),
    ({"items": "ip-in-ip"}, ([(4, "ip-in-ip")], [])),
    ({"items": 4}, ([(4, "ip-in-ip")], [])),
    ({"items": ["ipinip", "ip-in-ip"]}, ([(4, "ip-in-ip")], [])),
    ({"items": ["ip-in-ip", "ipinip"]}, ([(4, "ip-in-ip")], [])),
    # 0-255
    ({"items": "0-255"}, ([(-1, "ip")], [])),
    ({"items": ALL}, ([(-1, "ip")], [])),
    ({"items": ALL, "verbose": False}, ([(-1, "ip")], [])),
    ({"items": ALL, "verbose": True}, (ip.ALL_PAIRS, [])),
    # -1
    ({"items": -1}, ([(-1, "ip")], [])),
    ({"items": "-1"}, ([(-1, "ip")], [])),
    ({"items": [-1]}, ([(-1, "ip")], [])),
    ({"items": ["-1"]}, ([(-1, "ip")], [])),
    ({"items": [-1, 2]}, ([(-1, "ip")], [])),
    ({"items": ["-1", "2"]}, ([(-1, "ip")], [])),
    ({"items": [-1], "verbose": False}, ([(-1, "ip")], [])),
    # ip
    ({"items": "ip"}, ([(-1, "ip")], [])),
    ({"items": "ip", "verbose": False}, ([(-1, "ip")], [])),
    ({"items": "ip", "verbose": True}, (ip.ALL_PAIRS, [])),
    ({"items": "ip,icmp"}, ([(-1, "ip")], [])),
    ({"items": ["ip", "icmp"]}, ([(-1, "ip")], [])),
    ({"items": ["ip", "icmp"], "verbose": True}, (ip.ALL_PAIRS, [])),
    # undefined
    ({"items": ["typo"]}, ([], ["typo"])),
    ({"items": [256]}, ([], ["256"])),
    ({"items": ["typo", 256, 1]}, ([(1, "icmp")], ["256", "typo"])),
    ({"items": [*ALL, 256]}, ([(-1, "ip")], ["256"])),
    ({"items": [*ALL, 256], "verbose": True}, (ip.ALL_PAIRS, ["256"])),
    # combo
    ({"items": "typo,1,ipinip,255,256"},
     ([(1, "icmp"), (4, "ipinip"), (255, "")], ["256", "typo"])),
    ({"items": "ipinip,ip-in-ip"}, ([(4, "ip-in-ip")], [])),
])
def test__ip_pairs(kwargs, expected):
    """ip.ip_pairs()"""
    actual = ip.ip_pairs(**kwargs)

    diff = list(dictdiffer.diff(actual, expected))
    assert diff == []
