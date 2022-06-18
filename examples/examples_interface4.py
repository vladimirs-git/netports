"""Examples Interface4"""

from netports import Interface4

# Attributes demonstration
interface = Interface4("interface Ethernet1/2/3.4")
assert interface.line == "interface Ethernet1/2/3.4"
assert interface.name == "Ethernet1/2/3.4"
assert interface.id0 == "interface Ethernet"
assert interface.id1 == 1
assert interface.id2 == 2
assert interface.id3 == 3
assert interface.id4 == 4


# Interface with custom splitter between indexes. Splitter is ignored when comparing
interface1 = Interface4("interface Ethernet1/2/3.4")
interface2 = Interface4("interface Ethernet1-2-3+4", splitter="-+")
assert interface1 == interface2


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
for line in sorted(lines):
    print(line)
print()
# interface Ethernet1/1/1.1
# interface Ethernet1/2/1.1
# interface Ethernet1/20/1.1
# interface Ethernet1/3/1.1
# interface Ethernet10/1/1.1
# interface Ethernet2/1/1.1

# Sorting by indexes. This approach is useful in scripting
interfaces = [Interface4(line) for line in lines]
for interface in sorted(interfaces):
    print(interface)
print()
# interface Ethernet1/1/1.1
# interface Ethernet1/2/1.1
# interface Ethernet1/3/1.1
# interface Ethernet1/20/1.1
# interface Ethernet2/1/1.1
# interface Ethernet10/1/1.1


# Grouping interfaces by 3rd index
lines = [
    "interface Ethernet101/1/1",
    "interface Ethernet101/1/2",
    "interface Ethernet101/1/3",
    "interface Ethernet102/1/1",
    "interface Ethernet102/1/2",
    "interface Ethernet102/1/3",
]
interfaces = [Interface4(line) for line in lines]
interfaces.sort(key=lambda o: o.id3)
for interface in interfaces:
    print(interface)
print()
# interface Ethernet101/1/1
# interface Ethernet102/1/1
# interface Ethernet101/1/2
# interface Ethernet102/1/2
# interface Ethernet101/1/3
# interface Ethernet102/1/3
