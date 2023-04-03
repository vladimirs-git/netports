"""unittest helpers"""

# ========================== short_to_long ===========================
SHORT_TO_LONG = {
    "At": "ATM",
    "BAGG": "Bridge-Aggregation",
    "BE": "Bundle-Ether",
    "EO": "EOBC",
    "Eth": "Ethernet",
    "FD": "Fddi",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "GE": "GigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigabitEthernet",
    "Lo": "Loopback",
    "MFR": "MFR",
    "Ma": "Management",
    "Mg": "MgmtEth",
    "Mu": "Multilink",
    "Po": "Port-channel",
    "Se": "Serial",
    "Te": "TenGigabitEthernet",
    "Tu": "Tunnel",
    "Twe": "TwentyFiveGigE",
    "Two": "TwoGigabitEthernet",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vlan": "Vlan",
    "Vt": "Virtual-Template",
    "XGE": "Ten-GigabitEthernet",
    "mgmt": "mgmt",
    "ti": "tunnel-ip",
}
SHORT_TO_LONG_VALUE_LOW = {k: v.lower() for k, v in SHORT_TO_LONG.items()}
SHORT_TO_LONG_KEY_LOW = {k.lower(): v for k, v in SHORT_TO_LONG.items()}
SHORT_TO_LONG_ASR = {
    "At": "ATM",
    "BE": "Bundle-Ether",
    "EO": "EOBC",
    "Eth": "Ethernet",
    "FD": "Fddi",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigE",
    "Lo": "Loopback",
    "MFR": "MFR",
    "Ma": "Management",
    "Mg": "MgmtEth",
    "Mu": "Multilink",
    "Po": "Port-channel",
    "Se": "Serial",
    "Te": "TenGigE",
    "Tu": "tunnel-ip",
    "Twe": "TwentyFiveGigE",
    "Two": "TwoGigabitEthernet",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vlan": "Vlan",
    "Vt": "Virtual-Template",
    "ti": "tunnel-ip",
}
SHORT_TO_LONG_IOS = {
    "At": "ATM",
    "EO": "EOBC",
    "Eth": "Ethernet",
    "FD": "Fddi",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigabitEthernet",
    "Lo": "Loopback",
    "MFR": "MFR",
    "Ma": "Management",
    "Mu": "Multilink",
    "Po": "Port-channel",
    "Se": "Serial",
    "Te": "TenGigabitEthernet",
    "Tu": "Tunnel",
    "Twe": "TwentyFiveGigE",
    "Two": "TwoGigabitEthernet",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vlan": "Vlan",
    "Vt": "Virtual-Template",
}
SHORT_TO_LONG_NXOS = {
    "At": "ATM",
    "EO": "EOBC",
    "Eth": "Ethernet",
    "FD": "Fddi",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigabitEthernet",
    "Lo": "loopback",
    "MFR": "MFR",
    "Ma": "Management",
    "Mu": "Multilink",
    "Po": "port-channel",
    "Se": "Serial",
    "Te": "TenGigabitEthernet",
    "Tu": "Tunnel",
    "Twe": "TwentyFiveGigE",
    "Two": "TwoGigabitEthernet",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vlan": "Vlan",
    "Vt": "Virtual-Template",
    "mgmt": "mgmt",
}
SHORT_TO_LONG_H3C = {
    "At": "ATM",
    "BAGG": "Bridge-Aggregation",
    "EO": "EOBC",
    "Eth": "Ethernet",
    "FD": "Fddi",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "GE": "GigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigabitEthernet",
    "Lo": "Loopback",
    "MFR": "MFR",
    "Ma": "Management",
    "Mu": "Multilink",
    "Po": "Port-channel",
    "Se": "Serial",
    "Te": "Ten-GigabitEthernet",
    "Tu": "Tunnel",
    "Twe": "TwentyFiveGigE",
    "Two": "TwoGigabitEthernet",
    "V": "Vlan",
    "Vi": "Virtual-Access",
    "Vlan": "Vlan-interface",
    "Vt": "Virtual-Template",
    "XGE": "Ten-GigabitEthernet",
}

# ========================== short_to_short ==========================
SHORT_TO_SHORT = {
    "At": "At",
    "BAGG": "BAGG",
    "BE": "BE",
    "EO": "EO",
    "Eth": "Eth",
    "FD": "FD",
    "Fa": "Fa",
    "Fo": "Fo",
    "GE": "Gi",
    "Gi": "Gi",
    "Hu": "Hu",
    "Lo": "Lo",
    "MFR": "MFR",
    "Ma": "Ma",
    "Mg": "Mg",
    "Mu": "Mu",
    "Po": "Po",
    "Se": "Se",
    "Te": "Te",
    "Tu": "Tu",
    "Twe": "Twe",
    "Two": "Two",
    "V": "V",
    "Vi": "Vi",
    "Vlan": "V",
    "Vt": "Vt",
    "XGE": "XGE",
    "mgmt": "mgmt",
    "ti": "ti",
}
SHORT_TO_SHORT_VALUE_LOW = {k: v.lower() for k, v in SHORT_TO_SHORT.items()}
SHORT_TO_SHORT_KEY_LOW = {k.lower(): v for k, v in SHORT_TO_SHORT.items()}
SHORT_TO_SHORT_ASR = {
    "At": "At",
    "BE": "BE",
    "EO": "EO",
    "Eth": "Eth",
    "FD": "FD",
    "Fa": "Fa",
    "Fo": "Fo",
    "Gi": "Gi",
    "Hu": "Hu",
    "Lo": "Lo",
    "MFR": "MFR",
    "Ma": "Ma",
    "Mg": "Mg",
    "Mu": "Mu",
    "Po": "Po",
    "Se": "Se",
    "Te": "Te",
    "Tu": "ti",
    "Twe": "Twe",
    "Two": "Two",
    "V": "Vlan",
    "Vi": "Vi",
    "Vlan": "Vlan",
    "Vt": "Vt",
    "ti": "ti",
}
SHORT_TO_SHORT_IOS = {
    "At": "At",
    "EO": "EO",
    "Eth": "Eth",
    "FD": "FD",
    "Fa": "Fa",
    "Fo": "Fo",
    "Gi": "Gi",
    "Hu": "Hu",
    "Lo": "Lo",
    "MFR": "MFR",
    "Ma": "Ma",
    "Mu": "Mu",
    "Po": "Po",
    "Se": "Se",
    "Te": "Te",
    "Tu": "Tu",
    "Twe": "Twe",
    "Two": "Two",
    "V": "Vlan",
    "Vi": "Vi",
    "Vlan": "Vlan",
    "Vt": "Vt",
}
SHORT_TO_SHORT_NXOS = {
    "At": "At",
    "EO": "EO",
    "Eth": "Eth",
    "FD": "FD",
    "Fa": "Fa",
    "Fo": "Fo",
    "Gi": "Gi",
    "Hu": "Hu",
    "Lo": "Lo",
    "MFR": "MFR",
    "Ma": "Ma",
    "Mu": "Mu",
    "Po": "Po",
    "Se": "Se",
    "Te": "Te",
    "Tu": "Tu",
    "Twe": "Twe",
    "Two": "Two",
    "V": "Vlan",
    "Vi": "Vi",
    "Vlan": "Vlan",
    "Vt": "Vt",
    "mgmt": "mgmt",
}
SHORT_TO_SHORT_H3C = {
    "At": "At",
    "BAGG": "BAGG",
    "EO": "EO",
    "Eth": "Eth",
    "FD": "FD",
    "Fa": "Fa",
    "Fo": "Fo",
    "GE": "GE",
    "Gi": "GE",
    "Hu": "Hu",
    "Lo": "Lo",
    "MFR": "MFR",
    "Ma": "Ma",
    "Mu": "Mu",
    "Po": "Po",
    "Se": "Se",
    "Te": "XGE",
    "Tu": "Tu",
    "Twe": "Twe",
    "Two": "Two",
    "V": "V",
    "Vi": "Vi",
    "Vlan": "Vlan",
    "Vt": "Vt",
    "XGE": "XGE",
}

# ========================== long_to_short ===========================
LONG_TO_SHORT = {
    "ATM": "At",
    "Bridge-Aggregation": "BAGG",
    "Bundle-Ether": "BE",
    "EOBC": "EO",
    "Ethernet": "Eth",
    "FastEthernet": "Fa",
    "Fddi": "FD",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "Gi",
    "HundredGigabitEthernet": "Hu",
    "Loopback": "Lo",
    "MFR": "MFR",
    "Management": "Ma",
    "MgmtEth": "Mg",
    "Multilink": "Mu",
    "Port-channel": "Po",
    "Serial": "Se",
    "Ten-GigabitEthernet": "XGE",
    "TenGigabitEthernet": "Te",
    "Tunnel": "Tu",
    "TwentyFiveGigE": "Twe",
    "TwoGigabitEthernet": "Two",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
    "Vlan": "V",
    "mgmt": "mgmt",
    "tunnel-ip": "ti",
}
LONG_TO_SHORT_VALUE_LOW = {k: v.lower() for k, v in LONG_TO_SHORT.items()}
LONG_TO_SHORT_KEY_LOW = {k.lower(): v for k, v in LONG_TO_SHORT.items()}
LONG_TO_SHORT_ASR = {
    "ATM": "At",
    "Bundle-Ether": "BE",
    "EOBC": "EO",
    "Ethernet": "Eth",
    "FastEthernet": "Fa",
    "Fddi": "FD",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "Gi",
    "HundredGigE": "Hu",
    "Loopback": "Lo",
    "MFR": "MFR",
    "Management": "Ma",
    "MgmtEth": "Mg",
    "Multilink": "Mu",
    "Port-channel": "Po",
    "Serial": "Se",
    "TenGigE": "Te",
    "Tunnel": "ti",
    "TwentyFiveGigE": "Twe",
    "TwoGigabitEthernet": "Two",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
    "Vlan": "Vlan",
    "tunnel-ip": "ti",
    'HundredGigabitEthernet': 'Hu',
    'TenGigabitEthernet': "Te",
}
LONG_TO_SHORT_IOS = {
    "ATM": "At",
    "EOBC": "EO",
    "Ethernet": "Eth",
    "FastEthernet": "Fa",
    "Fddi": "FD",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "Gi",
    "HundredGigabitEthernet": "Hu",
    "Loopback": "Lo",
    "MFR": "MFR",
    "Management": "Ma",
    "Multilink": "Mu",
    "Port-channel": "Po",
    "Serial": "Se",
    "TenGigabitEthernet": "Te",
    "Tunnel": "Tu",
    "TwentyFiveGigE": "Twe",
    "TwoGigabitEthernet": "Two",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
    "Vlan": "Vlan",
}
LONG_TO_SHORT_NXOS = {
    "ATM": "At",
    "EOBC": "EO",
    "Ethernet": "Eth",
    "FastEthernet": "Fa",
    "Fddi": "FD",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "Gi",
    "HundredGigabitEthernet": "Hu",
    "Loopback": "Lo",
    "MFR": "MFR",
    "Management": "Ma",
    "Multilink": "Mu",
    "Port-channel": "Po",
    "Serial": "Se",
    "TenGigabitEthernet": "Te",
    "Tunnel": "Tu",
    "TwentyFiveGigE": "Twe",
    "TwoGigabitEthernet": "Two",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
    "Vlan": "Vlan",
    "loopback": "Lo",
    "mgmt": "mgmt",
    "port-channel": "Po",
}
LONG_TO_SHORT_H3C = {
    "ATM": "At",
    "Bridge-Aggregation": "BAGG",
    "EOBC": "EO",
    "Ethernet": "Eth",
    "FastEthernet": "Fa",
    "Fddi": "FD",
    "FortyGigabitEthernet": "Fo",
    "GigabitEthernet": "GE",
    "HundredGigabitEthernet": "Hu",
    "Loopback": "Lo",
    "MFR": "MFR",
    "Management": "Ma",
    "Multilink": "Mu",
    "Port-channel": "Po",
    "Serial": "Se",
    "Ten-GigabitEthernet": "XGE",
    "TenGigabitEthernet": "XGE",
    "Tunnel": "Tu",
    "TwentyFiveGigE": "Twe",
    "TwoGigabitEthernet": "Two",
    "Virtual-Access": "Vi",
    "Virtual-Template": "Vt",
    "Vlan": "V",
    "Vlan-interface": "Vlan",
}
LONG_TO_LONG = {
    "ATM": "ATM",
    "Bridge-Aggregation": "Bridge-Aggregation",
    "Bundle-Ether": "Bundle-Ether",
    "EOBC": "EOBC",
    "Ethernet": "Ethernet",
    "FastEthernet": "FastEthernet",
    "Fddi": "Fddi",
    "FortyGigabitEthernet": "FortyGigabitEthernet",
    "GigabitEthernet": "GigabitEthernet",
    "HundredGigabitEthernet": "HundredGigabitEthernet",
    "Loopback": "Loopback",
    "MFR": "MFR",
    "Management": "Management",
    "MgmtEth": "MgmtEth",
    "Multilink": "Multilink",
    "Port-channel": "Port-channel",
    "Serial": "Serial",
    "Ten-GigabitEthernet": "Ten-GigabitEthernet",
    "TenGigabitEthernet": "TenGigabitEthernet",
    "Tunnel": "Tunnel",
    "TwentyFiveGigE": "TwentyFiveGigE",
    "TwoGigabitEthernet": "TwoGigabitEthernet",
    "Virtual-Access": "Virtual-Access",
    "Virtual-Template": "Virtual-Template",
    "Vlan": "Vlan",
    "mgmt": "mgmt",
    "tunnel-ip": "tunnel-ip",
}
LONG_TO_LONG_VALUE_LOW = {k: v.lower() for k, v in LONG_TO_LONG.items()}
LONG_TO_LONG_KEY_LOW = {k.lower(): v for k, v in LONG_TO_LONG.items()}
LONG_TO_LONG_ASR = {
    "ATM": "ATM",
    "Bundle-Ether": "Bundle-Ether",
    "EOBC": "EOBC",
    "Ethernet": "Ethernet",
    "FastEthernet": "FastEthernet",
    "Fddi": "Fddi",
    "FortyGigabitEthernet": "FortyGigabitEthernet",
    "GigabitEthernet": "GigabitEthernet",
    "HundredGigE": "HundredGigE",
    "Loopback": "Loopback",
    "MFR": "MFR",
    "Management": "Management",
    "MgmtEth": "MgmtEth",
    "Multilink": "Multilink",
    "Port-channel": "Port-channel",
    "Serial": "Serial",
    "TenGigE": "TenGigE",
    "TwentyFiveGigE": "TwentyFiveGigE",
    "TwoGigabitEthernet": "TwoGigabitEthernet",
    "Virtual-Access": "Virtual-Access",
    "Virtual-Template": "Virtual-Template",
    "Vlan": "Vlan",
    "tunnel-ip": "tunnel-ip",
}
LONG_TO_LONG_IOS = {
    "ATM": "ATM",
    "EOBC": "EOBC",
    "Ethernet": "Ethernet",
    "FastEthernet": "FastEthernet",
    "Fddi": "Fddi",
    "FortyGigabitEthernet": "FortyGigabitEthernet",
    "GigabitEthernet": "GigabitEthernet",
    "HundredGigabitEthernet": "HundredGigabitEthernet",
    "Loopback": "Loopback",
    "MFR": "MFR",
    "Management": "Management",
    "Multilink": "Multilink",
    "Port-channel": "Port-channel",
    "Serial": "Serial",
    "TenGigabitEthernet": "TenGigabitEthernet",
    "Tunnel": "Tunnel",
    "TwentyFiveGigE": "TwentyFiveGigE",
    "TwoGigabitEthernet": "TwoGigabitEthernet",
    "Virtual-Access": "Virtual-Access",
    "Virtual-Template": "Virtual-Template",
    "Vlan": "Vlan",
}
LONG_TO_LONG_NXOS = {
    "ATM": "ATM",
    "EOBC": "EOBC",
    "Ethernet": "Ethernet",
    "FastEthernet": "FastEthernet",
    "Fddi": "Fddi",
    "FortyGigabitEthernet": "FortyGigabitEthernet",
    "GigabitEthernet": "GigabitEthernet",
    "HundredGigabitEthernet": "HundredGigabitEthernet",
    "MFR": "MFR",
    "Management": "Management",
    "Multilink": "Multilink",
    "Serial": "Serial",
    "TenGigabitEthernet": "TenGigabitEthernet",
    "Tunnel": "Tunnel",
    "TwentyFiveGigE": "TwentyFiveGigE",
    "TwoGigabitEthernet": "TwoGigabitEthernet",
    "Virtual-Access": "Virtual-Access",
    "Virtual-Template": "Virtual-Template",
    "Vlan": "Vlan",
    "loopback": "loopback",
    "mgmt": "mgmt",
    "port-channel": "port-channel",
}
LONG_TO_LONG_H3C = {
    "ATM": "ATM",
    "Bridge-Aggregation": "Bridge-Aggregation",
    "EOBC": "EOBC",
    "Ethernet": "Ethernet",
    "FastEthernet": "FastEthernet",
    "Fddi": "Fddi",
    "FortyGigabitEthernet": "FortyGigabitEthernet",
    "GigabitEthernet": "GigabitEthernet",
    "HundredGigabitEthernet": "HundredGigabitEthernet",
    "Loopback": "Loopback",
    "MFR": "MFR",
    "Management": "Management",
    "Multilink": "Multilink",
    "Port-channel": "Port-channel",
    "Serial": "Serial",
    "Ten-GigabitEthernet": "Ten-GigabitEthernet",
    "Tunnel": "Tunnel",
    "TwentyFiveGigE": "TwentyFiveGigE",
    "TwoGigabitEthernet": "TwoGigabitEthernet",
    "Virtual-Access": "Virtual-Access",
    "Virtual-Template": "Virtual-Template",
    "Vlan": "Vlan",
    "Vlan-interface": "Vlan-interface",
}