"""Examples Intf"""
from pprint import pprint

import netports
from netports import Intf

# Attributes demonstration
intf = Intf("interface Ethernet1/2/3.4")
assert intf.line == "interface Ethernet1/2/3.4"
assert intf.name == "Ethernet1/2/3.4"
assert intf.ids == ("interface Ethernet", "1", "2", "3", "4")
assert intf.delimiters == ("/", "/", ".")
assert intf.id0 == "interface Ethernet"
assert intf.id1 == 1
assert intf.id2 == 2
assert intf.id3 == 3
assert intf.id4 == 4

# Methods
print("last_idx", intf.last_idx())
print("name_short", intf.name_short())
print("name_long", intf.name_long())
print("name_full", intf.name_full())
print("part before id", intf.part_before(idx=3))
print("part before id", intf.part_before(idx=4))
print("part before id", intf.part_before(idx=4, splitter=False))
print("part after id", intf.part_before(idx=3))
print("part after id", intf.part_before(idx=3, splitter=False))
print()
# last_idx 4
# name_short Eth1/2/3.4
# name_long Ethernet1/2/3.4
# name_full interface Ethernet1/2/3.4
# part before id interface Ethernet1/2/
# part before id interface Ethernet1/2/3.
# part before id interface Ethernet1/2/3
# part after id interface Ethernet1/2/
# part after id interface Ethernet1/2


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
intfs = [Intf(line) for line in lines]
pprint(intfs, width=50)
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
intfs = [Intf(line) for line in lines]
intfs.sort(key=lambda o: o.id3)
pprint(intfs, width=50)
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

# Interface name mapping long-to-short
long_to_short = netports.long_to_short()
pprint(long_to_short, width=50)
print()
# {"Ethernet": "Eth",
#  "FastEthernet": "Fa",
#  "GigabitEthernet": "Gi",
#  ...

# Interface name mapping short-to-long
short_to_long = netports.short_to_long()
pprint(short_to_long, width=50)
print()
# {"Eth": "Ethernet",
#  "Fa": "FastEthernet",
#  "Gi": "GigabitEthernet",
#  ...
