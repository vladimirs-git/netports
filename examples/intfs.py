"""Examples Intf"""
from pprint import pprint

import netports
from netports import Intf

# Attributes demonstration
interface = Intf("interface Ethernet1/2/3.4")
assert interface.line == "interface Ethernet1/2/3.4"
assert interface.name == "Ethernet1/2/3.4"
assert interface.ids == ('interface Ethernet', '1', '2', '3', '4')
assert interface.delimiters == ('/', '/', '.')
assert interface.id0 == "interface Ethernet"
assert interface.id1 == 1
assert interface.id2 == 2
assert interface.id3 == 3
assert interface.id4 == 4

# Methods
print("last_idx", interface.last_idx())
print("name_short", interface.name_short())
print("part before id", 2, interface.part(2))
print()
# last_idx 4
# name_short Eth1/2/3.4
# part before id 2 interface Ethernet1/


# Sorting by indexes
lines = [
    "interface Ethernet1/1/1.1",
    "interface Ethernet10/1/1.1",
    "interface Ethernet2/1/1.1",
    "interface Ethernet1/2/1.1",
    "interface Ethernet1/20/1.1",
    "interface Ethernet1/3/1.1",
]

# Alphabetical sorting. This approach is not convenient in scripting
pprint(lines, width=50)
print()
# ["interface Ethernet1/1/1.1",
#  "interface Ethernet10/1/1.1",
#  "interface Ethernet2/1/1.1",
#  "interface Ethernet1/2/1.1",
#  "interface Ethernet1/20/1.1",
#  "interface Ethernet1/3/1.1"]

# Sorting by indexes. This approach is useful in scripting
interfaces = [Intf(line) for line in lines]
pprint(interfaces, width=50)
print()
# [Intf("interface Ethernet1/1/1.1"),
#  Intf("interface Ethernet10/1/1.1"),
#  Intf("interface Ethernet2/1/1.1"),
#  Intf("interface Ethernet1/2/1.1"),
#  Intf("interface Ethernet1/20/1.1"),
#  Intf("interface Ethernet1/3/1.1")]


# Grouping interfaces by 3rd index
lines = [
    "interface Ethernet101/1/1",
    "interface Ethernet101/1/2",
    "interface Ethernet101/1/3",
    "interface Ethernet102/1/1",
    "interface Ethernet102/1/2",
    "interface Ethernet102/1/3",
]
interfaces = [Intf(line) for line in lines]
interfaces.sort(key=lambda o: o.id3)
pprint(interfaces, width=50)
print()
# [Intf("interface Ethernet101/1/1"),
#  Intf("interface Ethernet102/1/1"),
#  Intf("interface Ethernet101/1/2"),
#  Intf("interface Ethernet102/1/2"),
#  Intf("interface Ethernet101/1/3"),
#  Intf("interface Ethernet102/1/3")]


# Interface ranges with long notation
ranges = netports.intfrange(lines)
pprint(ranges, width=50)
print()
# ["interface Ethernet101/1/1-3",
#  "interface Ethernet102/1/1-3"]

# Interface ranges with short notation
ranges = netports.intfrange(lines, fmt="short")
pprint(ranges, width=30)
print()
# ["Eth101/1/1-3",
#  "Eth102/1/1-3"]
