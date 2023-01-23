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
    "Vlan": ["Vl", "V"],  # Cisco IOS
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
long_to_short = {k: ls[0] for k, ls in long_to_shorts.items()}
long_to_short_lower: DStr = {k.lower(): v for k, v in long_to_short.items()}
short_to_long: DStr = {v: k for k, v in long_to_short.items()}
short_to_long_lower: DStr = {k.lower(): v for k, v in short_to_long.items()}
