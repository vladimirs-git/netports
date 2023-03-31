"""Interface name mapping"""
from netports.types_ import DStr, DLStr

long_to_shorts: DLStr = {
    # ethernets
    "FastEthernet": ["Fa"],  # Cisco IOS
    "FortyGigabitEthernet": ["Fo"],
    "GigabitEthernet": ["Gi"],  # Cisco IOS
    "HundredGigabitEthernet": ["Hu"],
    "TenGigabitEthernet": ["Te"],  # Cisco IOS
    "TwoGigabitEthernet": ["Two"],
    "Wlan-GigabitEthernet": ["Wl-Gi"],
    "Ethernet": ["Eth"],  # Cisco NX-OS
    # other frequently used
    "Tunnel-ip": ["Tu"],  # Cisco ASR9000
    "Tunnel": ["Tu"],  # Cisco IOS
    "Port-channel": ["Po"],  # Cisco IOS
    "Loopback": ["Lo"],  # Cisco IOS
    "Vlan": ["V", "Vl"],  # Cisco IOS
    # other rear
    "ATM": ["At"],
    "EOBC": ["EO"],
    "Fddi": ["FD"],
    "MFR": ["MFR"],
    "Management": ["Ma"],
    "Multilink": ["Mu"],
    # "POS": ["PO"],  # conflict with Port-channel
    "Serial": ["Se"],
    "TwentyFiveGigE": ["Twe"],
    "Virtual-Access": ["Vi"],
    "Virtual-Template": ["Vt"],
}
long_to_long_lower = {lng.lower(): lng for lng in long_to_shorts}
long_to_short = {lng: ls[0] for lng, ls in long_to_shorts.items()}  # single value
long_to_short_lower: DStr = {lng.lower(): short for lng, short in long_to_short.items()}
short_to_long: DStr = {short: lng for lng, ls in long_to_shorts.items() for short in ls}
short_to_long_lower: DStr = {short.lower(): lng for short, lng in short_to_long.items()}
short_to_short: DStr = {short.lower(): ls[0] for ls in long_to_shorts.values() for short in ls}

# platform cisco_asr
short_to_long__cisco_asr: DStr = short_to_long.copy()
short_to_long__cisco_asr["Tu"] = "Tunnel-ip"
short_to_long_lower__cisco_asr: DStr = short_to_long_lower.copy()
short_to_long_lower__cisco_asr["tu"] = "Tunnel-ip"


def get_short_to_long(platform: str = "") -> DStr:
    """Returns Interfaces map of short_to_long by platform
    ::
        :param platform: Platform
        :return: Interfaces map of short_to_long
    """
    if platform == "cisco_asr":
        return short_to_long__cisco_asr
    return short_to_long


def get_short_to_long_lower(platform: str = "") -> DStr:
    """Returns Interfaces map of short_to_long by platform
    ::
        :param platform: Platform
        :return: Interfaces map of short_to_long
    """
    if platform == "cisco_asr":
        return short_to_long_lower__cisco_asr
    return short_to_long_lower
