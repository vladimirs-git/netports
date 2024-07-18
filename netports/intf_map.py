"""Interface name mapping"""
from netports.types_ import DStr, LStr, SStr, OBool

MAP_OTHER = {  # parent of all
    "At": "ATM",
    "Bu": "BundleEthernet",
    "FD": "Fddi",
    "Hu": "HundredGigabitEthernet",  # overlapped ios
    "Ma": "Management",
    "Mu": "Multilink",
    "Se": "Serial",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vt": "Virtual-Template",
}
MAP_CISCO_IOS = {  # parent of nxos, xr
    "Ap": "AppGigabitEthernet",  # Application Hosting
    "Em": "Embedded-Service-Engine",
    "Eth": "Ethernet",
    "Fa": "FastEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigE",  # overlapped: other
    "Lo": "Loopback",  # overlapped: nxos
    "Po": "Port-channel",  # overlapped: nxos
    "Te": "TenGigabitEthernet",  # overlapped: xr
    "Tu": "Tunnel",  # overlapped: xr
    "Twe": "TwentyFiveGigE",
    "Vlan": "Vlan",  # overlapped: h3c
}
MAP_CISCO_NXOS = {
    "Po": "port-channel",  # overlapped: ios
    "Lo": "loopback",  # overlapped: ios, xr
    "mgmt": "mgmt",
}
MAP_CISCO_XR = {
    "Te": "TenGigE",  # overlapped: ios
    "BE": "Bundle-Ether",
    "Tu": "tunnel-ip",  # low-priority, overlapped: ios, nxos
    "ti": "tunnel-ip",
    "Mg": "MgmtEth",
}
MAP_HP_COMWARE = {  # h3c
    "GE": "GigabitEthernet",
    "Te": "Ten-GigabitEthernet",  # low-priority, overlapped: ios
    "XGE": "Ten-GigabitEthernet",
    "BAGG": "Bridge-Aggregation",
    "Vlan": "Vlan-interface",  # overlapped: ios
}
MAP_HP_PROCURVE = {  # hpc
    "Trk": "Trk",
}
ALL_SHORT = sorted(
    {
        *MAP_OTHER,
        *MAP_CISCO_IOS,
        *MAP_CISCO_NXOS,
        *MAP_CISCO_XR,
        *MAP_HP_COMWARE,
        *MAP_HP_PROCURVE,
    }
)


def long_to_short(
    device_type: str = "", key_lower: bool = False, value_lower: bool = False
) -> DStr:
    """Return Interfaces map long-to-short, device_type specific.

    :param device_type: Netmiko device type.
    :param key_lower: True - keys lower-case, False - keys upper-case.
    :param value_lower: True - values lower-case, False - values upper-case.
    :return: Interfaces map.

    :example:
        long_to_short() -> {"Vlan": "V", ...}
        long_to_short(device_type="cisco_ios") -> {"Vlan": "Vlan", ...}
        long_to_short(device_type="cisco_ios", key_lower=True) -> {"vlan": "Vlan", ...}
    """
    data: DStr = short_to_long(device_type=device_type)
    data = {v: k for k, v in data.items()}
    data_ = _overlapped(data)
    data.update(data_)

    if device_type == "cisco_xr":
        data["Tunnel"] = "ti"
    elif device_type == "hp_comware":
        data["TenGigabitEthernet"] = "XGE"

    data = _lower(data, key_lower, value_lower)
    return data


def long_to_long(device_type: str = "", key_lower: bool = False, value_lower: bool = False) -> DStr:
    """Return Interfaces map long-to-long, device_type specific.

    :param device_type: Netmiko device type.
    :param key_lower: True - keys lower-case, False - keys upper-case.
    :param value_lower: True - values lower-case, False - values upper-case.
    :return: Interfaces map.
    """
    data: DStr = short_to_long(device_type=device_type)
    data = {v: k for k, v in data.items()}
    data = {k: k for k in data}
    data = _lower(data, key_lower, value_lower)
    return data


def longs(device_type: str = "", value_lower: OBool = None) -> LStr:
    """Return long names of all interfaces.

    :param device_type: Netmiko device type.
    :param value_lower: True - values lower-case, False - values upper-case.
        Default is None, lower-case and upper-case.
    :return: Long names of all interfaces.

    :example:
        longs() -> ["ATM", "Bridge-Aggregation", "Bundle-Ether", ...]
        longs(device_type="cisco_ios") ->["ATM", "Ethernet", "FastEthernet", ...]
        longs(device_type="cisco_ios", value_lower=True) -> ["atm", "ethernet", ...]
    """
    if value_lower is None:
        upper: SStr = set(long_to_long(device_type=device_type, key_lower=False))
        lower: SStr = set(long_to_long(device_type=device_type, key_lower=True))
        return sorted(upper.union(lower))
    if value_lower:
        return sorted(long_to_long(device_type=device_type, key_lower=True))
    return sorted(long_to_long(device_type=device_type, key_lower=False))


def short_to_long(
    device_type: str = "", key_lower: bool = False, value_lower: bool = False
) -> DStr:
    """Return Interfaces map short-to-long, device_type specific.

    :param device_type: Netmiko device type.
    :param key_lower: True - keys lower-case, False - keys upper-case.
    :param value_lower: True - values lower-case, False - values upper-case.
    :return: Interfaces map.

    :example:
        short_to_long() -> {"Fa": "FastEthernet", ...}
        short_to_long(key_lower=True) -> {"fa": "FastEthernet", ...}
        short_to_long(value_lower=True) -> {"Fa": "fastethernet", ...}
    """
    if device_type == "cisco_xr":
        data = MAP_OTHER.copy()
        data.update(MAP_CISCO_IOS)
        data.update(MAP_CISCO_XR)
    elif device_type == "cisco_ios":
        data = MAP_OTHER.copy()
        data.update(MAP_CISCO_IOS)
    elif device_type == "cisco_nxos":
        data = MAP_OTHER.copy()
        data.update(MAP_CISCO_IOS)
        data.update(MAP_CISCO_NXOS)
    elif device_type == "hp_comware":  # h3c
        data = MAP_OTHER.copy()
        data.update(MAP_CISCO_IOS)
        data.update(MAP_HP_COMWARE)
    elif device_type == "hp_procurve":  # h3c
        data = MAP_OTHER.copy()
        data.update(MAP_CISCO_IOS)
        data.update(MAP_HP_PROCURVE)
    else:
        data = MAP_HP_COMWARE.copy()
        data.update(MAP_HP_PROCURVE)
        data.update(MAP_CISCO_XR)
        data.update(MAP_CISCO_NXOS)
        data.update(MAP_CISCO_IOS)
        data.update(MAP_OTHER)
    data = _lower(data, key_lower, value_lower)
    return data


def short_to_short(
    device_type: str = "", key_lower: bool = False, value_lower: bool = False
) -> DStr:
    """Return Interfaces map short-to-short, device_type specific.

    :param device_type: Netmiko device type.
    :param key_lower: True - keys lower-case, False - keys upper-case.
    :param value_lower: True - values lower-case, False - values upper-case.
    :return: Interfaces map.

    :example:
        short_to_short(key_lower=True) -> {"fa": "Fa", ...}
        short_to_short(value_lower=True) -> {"Fa": "fa", ...}
    """
    data: DStr = short_to_long(device_type=device_type)
    data = {k: k for k in data}
    intf_map_l2s: DStr = long_to_short(device_type=device_type)
    intf_map_s2l: DStr = short_to_long(device_type=device_type)
    for short_upper, long_upper in intf_map_s2l.items():
        if value := intf_map_l2s.get(long_upper):
            data[short_upper] = value
    data = _lower(data, key_lower, value_lower)
    return data


def shorts(device_type: str = "", value_lower: OBool = None) -> LStr:
    """Return short names of all interfaces.

    :param device_type: Netmiko device type.
    :param value_lower: True - values lower-case, False - values upper-case.
        Default is None, lower-case and upper-case.
    :return: Short names of all interfaces.

    :example:
        shorts() -> ["At", "BAGG", "BE", ...]
        shorts(device_type="cisco_ios") -> ["At", "Eth", "Fa", ...]
        shorts(device_type="cisco_ios", value_lower=True) -> ["at", "eth", "fa", ...]
    """
    if value_lower is None:
        upper: SStr = set(short_to_short(device_type=device_type, key_lower=False))
        lower: SStr = set(short_to_short(device_type=device_type, key_lower=True))
        return sorted(upper.union(lower))
    if value_lower:
        return sorted(short_to_short(device_type=device_type, key_lower=True))
    return sorted(short_to_short(device_type=device_type, key_lower=False))


# ============================== helper ==============================


def _overlapped(data: DStr) -> DStr:
    """Return Interfaces map long-to-short that overlapped with short key in other device_type."""
    data_ = {v: k for k, v in MAP_OTHER.items()}
    data_.update({v: k for k, v in MAP_CISCO_IOS.items()})
    data_ = {k: v for k, v in data_.items() if k not in data}
    return data_


def _lower(data: DStr, key_lower: bool, value_lower: bool) -> DStr:
    """Change key, value to lower-case.

    :param data: Interfaces map data.
    :param key_lower: True - keys lower-case, False - keys upper-case.
    :param value_lower: True - values lower-case, False - values upper-case.
    """
    if key_lower:
        data = {k.lower(): v for k, v in data.items()}
    if value_lower:
        data = {k: v.lower() for k, v in data.items()}
    return data
