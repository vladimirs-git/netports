"""Interface name mapping"""
from netports.types_ import DStr

long_to_short: DStr = {
    # sorted ethernet
    "FastEthernet": "Fa",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "Gi",
    "HundredGigabitEthernet": "Hu",
    "TenGigabitEthernet": "Te",
    "TwoGigabitEthernet": "Two",
    "Wlan-GigabitEthernet": "Wl-Gi",
    "Ethernet": "Eth",
    # sorted tunnel
    "Tunnel-ip": "Tu",
    "Tunnel": "Tu",
    # frequently used
    "Port-channel": "Po",
    "Loopback": "Lo",
    "Vlan": "Vl",
    # other
    "ATM": "At",
    "EOBC": "EO",
    "Fddi": "FD",
    "MFR": "MFR",
    "Management": "Ma",
    "Multilink": "Mu",
    "POS": "PO",
    "Serial": "Se",
    "TwentyFiveGigE": "Twe",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
}
long_to_short_lower: DStr = {k.lower(): v for k, v in long_to_short.items()}
short_to_long: DStr = {v: k for k, v in long_to_short.items()}
short_to_long_lower: DStr = {k.lower(): v for k, v in short_to_long.items()}
