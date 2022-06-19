"""Examples IP protocols"""

from pprint import pprint

import netports

# IP_NAMES
pprint(netports.IP_NAMES)
#  'icmp': {'description': 'Internet Control Message Protocol, RFC 792',
#           'name': 'icmp',
#           'number': 1},
#  'tcp': {'description': 'Transmission Control Protocol, RFC 793',
#          'name': 'tcp',
#          'number': 6},
# ...

# IP_NUMBERS
pprint(netports.IP_NUMBERS)
# {0: {'description': 'IPv6 Hop-by-Hop Option, RFC 8200',
#      'name': 'hopopt',
#      'number': 0},
#  6: {'description': 'Transmission Control Protocol, RFC 793',
#      'name': 'tcp',
#      'number': 6},
# ...


# iip(items, all)
ports = netports.iip("icmp,tcp,7,255")
print(ports)
# [1, 6, 7, 255]

ports = netports.iip(["icmp", "tcp,1", "6-7", 255])
print(ports)
# [1, 6, 7, 255]

ports = netports.iip(all=True)
print(ports)
# [0, 1, ..., 255]

try:
    netports.iip("265")
except ValueError as ex:
    print(ex)
# invalid_ip_numbers=[265], expected in range 0...255


# nip(items, strict)
ports = netports.nip("icmp,tcp,7,255")
print(ports)
# (["icmp", "tcp"], [7, 255])

ports = netports.nip(["icmp", "tcp", 7, 255])
print(ports)
# (["icmp", "tcp"], [7, 255])

try:
    netports.nip("icmp,typo")
except ValueError as ex:
    print(ex)
# invalid_ip_names=["typo"]


# sip(items, all)
ports = netports.sip("icmp,tcp,7,255")
print(ports)
# 1,6-7,255

ports = netports.sip(["icmp", "icmp,tcp,1", "6-7", 255])
print(ports)
# 1,6-7,255

ports = netports.sip([255, 255, 1, 6, 7])
print(ports)
# 1,6-7,255

ports = netports.sip(all=True)
print(ports)
# 0-255

try:
    netports.sip("265")
except ValueError as ex:
    print(ex)
# invalid_ip_numbers=[265], expected in range 0...255
