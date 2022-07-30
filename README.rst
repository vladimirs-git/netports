netports
========

A collection of Python objects and functions for managing ranges of VLANs,
TCP/UDP ports, IP protocol numbers, interfaces.
Recommended for scripting in telecommunications networks.

.. contents::

.. sectnum::


Installation
------------

Install the package from pypi.org release

.. code:: bash

    pip install netports

or install the package from github.com release

.. code:: bash

    pip install https://github.com/vladimirs-git/netports/archive/refs/tags/0.5.2.tar.gz

or install the package from github.com repository

.. code:: bash

    pip install git+https://github.com/vladimirs-git/netports@0.5.2


TCP/UDP ports
-------------


itcp(items, verbose, all)
.........................

**Integer TCP/UDP Ports** - Sorting TCP/UDP ports and removing duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of TCP/UDP ports, can be unsorted and with duplicates
verbose         *bool*                      True - all ports in verbose mode: [1, 2, ..., 65535], False - all ports in brief mode: [-1] (reduces RAM usage), by default False
all				*bool*						True - Returns all TCP/UDP ports: [1, 2, ..., 65535], or [-1] for verbose=False
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted TCP/UDP ports
Raises
	*ValueError* if TCP/UDP ports are outside valid range 1...65535

.. code:: python

	import netports

	ports = netports.itcp("80,20,21-22")
	print(ports)
	# [20, 21, 22, 80]

	ports = netports.itcp(["20-22", "80", 22])
	print(ports)
	# [20, 21, 22, 80]

	ports = netports.itcp(all=True)
	print(ports)
	# [1, 2, ..., 65535]

	try:
		netports.itcp("65536")
	except ValueError as ex:
		print(ex)
	# invalid_port=[65536], expected in range 1...65535


stcp(items, verbose, all)
.........................

**String TCP/UDP ports** - Sorting TCP/UDP ports and removing duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of TCP/UDP ports, can be unsorted and with duplicates
verbose         *bool*                      True - all ports in verbose mode: [1, 2, ..., 65535], False - all ports in brief mode: [-1] (reduces RAM usage), by default False
all				*bool*						True - Returns all TCP/UDP ports: "1-65535"
=============== =========================== ============================================================================

Return
	*str* of unique sorted TCP/UDP ports
Raises
	*ValueError* if TCP/UDP ports are outside valid range 1...65535

.. code:: python

	import netports

	ports = netports.stcp("80,20-21,80")
	print(ports)
	# 20-21,80

	ports = netports.stcp(["80", "20-21", "20"])
	print(ports)
	# 20-21,80

	ports = netports.stcp([80, 80, 20, 21])
	print(ports)
	# 20-21,80

	ports = netports.stcp(all=True)
	print(ports)
	# 1-65535

	try:
		netports.stcp("65536")
	except ValueError as ex:
		print(ex)
	# invalid_port=[65536], expected in range 1...65535


VLAN IDs
--------


ivlan(items, verbose, all, splitter, range_splitter, platform)
..............................................................

**Integer VLAN IDs** - Sorting VLANs and removing duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs, can be unsorted and with duplicates
verbose         *bool*                      True - all VLAN IDs in verbose mode: [1, 2, ..., 65535], False - all VLAN IDs in brief mode: [-1] (reduces RAM usage), by default False
all				*bool*						True - Returns all VLAN IDs: [1, 2, ..., 4094], or [-1] for verbose=False
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
platform		*str*						Set ``splitter`` and ``range_splitter`` to platform specific values. Defined: "cisco" (Cisco IOS), "hpe" (Hewlett Packard Enterprise).
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted VLANs
Raises
	*ValueError* if VLANs are outside valid range 1...4094

.. code:: python

	import re
	import netports

	config = """
	interface FastEthernet0/1
	  switchport mode trunk
	  switchport trunk allowed vlan 1,3-5
	  end
	"""
	trunk = re.findall("vlan(.+)", config)[0]  # " 1,3-5"
	vlans = netports.ivlan(trunk)
	print(vlans)
	# [1, 3, 4, 5]

	vlans = netports.ivlan(["1", "3-4", "4-5"])
	print(vlans)
	# [1, 3, 4, 5]

	ports = netports.ivlan(all=True)
	print(ports)
	# [1, 2, ..., 4094]

	vlans = netports.ivlan("1 3 to 5", platform="hpe")
	print(vlans)
	# [1, 3, 4, 5]

	vlans = netports.ivlan("1 3 to 5", splitter=" ", range_splitter=" to ")
	print(vlans)
	# [1, 3, 4, 5]

	try:
		netports.ivlan("4095")
	except ValueError as ex:
		print(ex)
	# invalid_vlan=[4095], expected in range 1...4094


svlan(items, verbose, all, splitter, range_splitter, platform)
..............................................................

**String VLAN IDs** - Sorting VLANs and removing duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs, can be unsorted and with duplicates
verbose         *bool*                      True - all VLAN IDs in verbose mode: [1, 2, ..., 65535], False - all VLAN IDs in brief mode: [-1] (reduces RAM usage), by default False
all				*bool*						True - Returns all VLAN IDs: "1-4094"
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
platform		*str*						Set ``splitter`` and ``range_splitter`` to platform specific values. Defined: "cisco" (Cisco IOS), "hpe" (Hewlett Packard Enterprise).
=============== =========================== ============================================================================

Return
	*str* of unique sorted VLANs
Raises
	*ValueError* if VLANs are outside valid range 1...4094

.. code:: python

	import netports

	vlans = netports.svlan("3-4,1,4-5")
	print(vlans)
	# 1,3-5

	vlans = netports.svlan(["1", "3-5", "3-4", "4-5"])
	print(vlans)
	# 1,3-5

	vlans = netports.svlan([1, 3, 4, 5])
	print(vlans)
	# 1,3-5

	ports = netports.svlan(all=True)
	print(ports)
	# 1-4094

	vlans = netports.svlan("1 3 to 5", platform="hpe")
	print(vlans)
	# 1 3 to 5

	vlans = netports.svlan("1 3 to 5", splitter=" ", range_splitter=" to ")
	print(vlans)
	# 1 3 to 5

	try:
		netports.svlan("4095")
	except ValueError as ex:
		print(ex)
	# invalid_vlan=[4095], expected in range 1...4094


IP protocols
------------


IP_NAMES, IP_NUMBERS
....................

Dictionary with known IP protocol names and IDs listed in https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers


.. code:: python

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


iip(items, verbose, all, strict)
................................

**Integer IP protocol numbers** - Sorts numbers and removes duplicates.


=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol numbers, can be unsorted and with duplicates, "ip" - Return all IP protocol numbers: [0, 1, ..., 255]
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1] (reduces RAM usage), by default False
strict          *bool*                      True - Raises ValueError, if the protocol is unknown, False - Skips unknown protocols, by default - True
all				*bool*						True - Return all IP protocol numbers: [0, 1, ..., 255]
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted IP protocol numbers
Raises
	*ValueError* if IP protocol numbers are outside valid range 0...255

.. code:: python

	import netports

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


sip(items, verbose, all)
........................

**String IP protocol numbers** - Sorts numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol numbers, can be unsorted and with duplicates. "ip" - mean all numbers in range 0...255.
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1] (reduces RAM usage), by default False
strict          *bool*                      True - Raises ValueError, if the protocol is unknown, False - Skips unknown protocols, by default - True
all				*bool*						True - Return all IP protocol numbers: "0-255"
=============== =========================== ============================================================================

Return
	*str* of unique sorted IP protocol numbers
Raises
	*ValueError* if IP protocol numbers are outside valid range 0...255

.. code:: python

	import netports

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


ip_pairs(items, strict)
.......................

**IP protocol Names and Numbers** - Splits items to names and numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol names and numbers, can be unsorted and with duplicates
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1] (reduces RAM usage), by default False
=============== =========================== ============================================================================

Return
	*List[Tuple[int, str]]* Pairs of IP protocol number and name,
	 *List[str]* Undefined protocol names and invalid numbers

.. code:: python

	import netports

	pairs, invalid = netports.ip_pairs("1,tcp,255,256,typo")
	print("pairs", pairs)
	print("invalid", invalid)
	# pairs [(1, 'icmp'), (6, 'tcp'), (255, '')]
	# invalid ['256', 'typo']


Objects
-------


Range(items, splitter, range_splitter, strict)
..............................................

**Range** - An object that converts items to *object* that represents range as *str* and as *List[int]*.
Object implements most of the `set <https://www.w3schools.com/python/python_ref_set.asp>`_ and
`list <https://www.w3schools.com/python/python_ref_list.asp>`_ methods that handle the Range.numbers attribute.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str*, *List[int]*			Range of numbers. Numbers can be unsorted and duplicated.
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
strict			*bool*						True - Raise ValueError, if in items is invalid item. False - Make Range without invalid items. By default True.
=============== =========================== ============================================================================

Attributes demonstration

.. code:: python

	from netports import Range

	range_o = Range("1,3-5")
	assert range_o.line == "1,3-5"
	assert str(range_o) == "1,3-5"
	assert range_o.numbers() == [1, 3, 4, 5]
	assert list(range_o) == [1, 3, 4, 5]
	assert Range("1,3-5") == Range([1, 3, 4, 5])

	# Raise ValueError if one of item is invalid
	try:
		Range("1,3-5,typo")
	except ValueError as ex:
		print(ex)
	# invalid item="typo" in line="1,3-5,typo"

	# Make Range without invalid items (not raise ValueError)
	range_o = Range("1,3-5,typo", strict=False)
	assert range_o.line == "1,3-5"


Sorts numbers and removes duplicates

.. code:: python

	from netports import Range

	ranges1 = Range("3-5,1")
	print(ranges1)
	# 1,3-5

	ranges2 = Range("3-5,1,3-5,1,3-4,4-5")
	print(ranges2)
	# 1,3-5

	assert ranges1 == ranges2


Range with custom splitters

.. code:: python

	from netports import Range

	range_o = Range("1, 3-5, 7-9", splitter=", ")
	assert range_o.line == "1, 3-5, 7-9"
	assert range_o.numbers() == [1, 3, 4, 5, 7, 8, 9]

	range_o = Range("1 3 to 5 7 to 9", splitter=" ", range_splitter=" to ")
	assert range_o.line == "1 3 to 5 7 to 9"
	assert range_o.numbers() == [1, 3, 4, 5, 7, 8, 9]


Range operators
:::::::::::::::

**Range** object implements:

- Arithmetic operators: ``+``, ``-``
- Reference to numbers in range by index

=============================== =========================== ============================================================
Operator                        Return                      Description
=============================== =========================== ============================================================
Range("1,4") + Range("3,5")     Range("1,3-5")              Add two objects
Range("1-5") - Range("2")		Range("1,3-5")              Subtract two objects
Range("1,3-5")[1]               3                           Get number by index
Range("1,3-5")[1:3]             [3, 4]                      Get numbers by slice
=============================== =========================== ============================================================

.. code:: python

	from netports import Range

	range_o = Range("1,3") + Range("3-5")
	assert str(range_o) == "1,3-5"

	range_o = Range("1-5") - Range("2")
	assert str(range_o) == "1,3-5"

	assert range_o[1] == 3
	assert range_o[1:3] == [3, 4]

	for number in Range("1,3-5"):
		print(number)
	# 1
	# 3
	# 4
	# 5


Range methods
:::::::::::::

**Range** object implements most of `set <https://www.w3schools.com/python/python_ref_set.asp>`_
and `list <https://www.w3schools.com/python/python_ref_list.asp>`_ methods.

=================================== ====================================================================================
Method				                Description
=================================== ====================================================================================
add(other)                          Adds other *Range* object to self
append(number)                      Appends number to self
clear()                             Removes all numbers from self
copy()                              Returns a copy of self *Range* object
difference(other)                   Returns the *Range* object of the difference between self and other *Range*
difference_update(other)            Removes other *Range* from self
discard(number)                     Removes the specified number from self *Range*
extend(numbers)                     Adds *List[int]* numbers to self
index(number)                       Returns index of number, raises ValueError if the number is not present in range
intersection(other)                 Returns *Range* which is the intersection of self and other *Range*
intersection_update(other)          Removes numbers of other *Range* in self, that are not present in other
isdisjoint(other)                   Returns whether self numbers and other *Range* numbers have intersection or not
issubset(other)                     Returns whether other *Range* numbers contains self numbers or not
issuperset(other)                   Returns whether self *Range* numbers contains other *Range* numbers set or not
pop()                               Removes and returns last number in *Range*, raises IndexError if list is empty or index is out of range
remove(number)                      Removes the specified number from self *Range*, raises ValueError if the numbers is not present
symmetric_difference(other)         Returns *Range* object with the symmetric differences of self and other *Range*
symmetric_difference_update(other)  Inserts the symmetric differences from self *Range* and other *Range*
update(other)                       Returns *Range* of the union of self *Range* and other *Range*
=================================== ====================================================================================

.. code:: python

	from netports import Range

	range_o = Range("1,3") + Range("3-5")
	print(range_o)
	# 1,3-5

	range_o.append(2)
	print(range_o)
	# 1-5

	print(range_o.difference(Range("2,4")))
	# 1,3,5

	range_o.difference_update(Range("2,4"))
	print(range_o)
	# 1,3,5

	range_o.discard(3)
	print(range_o)
	# 1,5

	range_o.extend([3, 4])
	print(range_o)
	# 1,3-5

	print(range_o.index(5))
	# 3

	print(range_o.intersection(Range("1-4")))
	# 1,3-4

	range_o.intersection_update(Range("1-4"))
	print(range_o)
	# 1,3-4

	print(range_o.pop())
	print(range_o)
	# 4
	# 1,3

	range_o.remove(3)
	print(range_o)
	# 1

	range_o.update(Range("3,4,5"))
	print(range_o)
	# 1,3-5


Numbers
-------

parse_range(line, splitter, range_splitter)
...........................................

**Parse Range** - Parses range from line. Removes white spaces considering splitters. Sorts numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
line         	*str*						Range of numbers, can be unsorted and with duplicates
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
	Range *object*

Sorts numbers and removes duplicates

.. code:: python

	import netports

	range_o = netports.parse_range("3\t- 5, 1 , 3-5\t,1\n")
	print(f"{range_o!r}")
	print(range_o.line)
	print(range_o.numbers())
	# Range("1,3-5")
	# 1,3-5
	# [1, 3, 4, 5]

Range with custom splitter and range_splitter

.. code:: python

	import netports

	range_o = netports.parse_range("1 3 to 5 1 3 to 5", splitter=" ", range_splitter=" to ")
	print(f"{range_o!r}")
	print(range_o.line)
	print(range_o.numbers())
	# Range("1 3 to 5", splitter=" ", range_splitter=" to ")
	# 1 3 to 5
	# [1, 3, 4, 5]


inumbers(items, splitter, range_splitter)
.........................................

**Integer Numbers** - Sorts numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of numbers, can be unsorted and with duplicates
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted numbers

Converts unsorted range to sorted *List[int]* without duplicates

.. code:: python

	import netports

	ports = netports.inumbers("3-5,1,3-5,1")
	print(ports)
	# [1, 3, 4, 5]

	ports = netports.inumbers(["3-5,1", "3-4", "1"])
	print(ports)
	# [1, 3, 4, 5]

	ports = netports.inumbers([3, 4, 5, 1, 3, 4, 5, 1])
	print(ports)
	# [1, 3, 4, 5]

Converts unsorted range to *List[int]* with custom splitters

.. code:: python

	import netports

	ports = netports.inumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
	print(ports)
	# [1, 3, 4, 5]


snumbers(items, splitter, range_splitter)
.........................................

**String Numbers** - Sorts numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of numbers, can be unsorted and with duplicates
splitter     	*str*						Separator character between items, by default ","
range_splitter	*str*						Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
	*str* of unique sorted numbers

Converts unsorted range to sorted *str* without duplicates

.. code:: python

	import netports

	ports = netports.snumbers("3-5,1,3-5,1")
	print(ports)
	# 1,3-5

	ports = netports.snumbers(["3-5,1", "3-4", "1"])
	print(ports)
	# 1,3-5

	ports = netports.snumbers([3, 4, 5, 1, 3, 4, 5, 1])
	print(ports)
	# 1,3-5

Converts unsorted range to *str* with custom splitters

.. code:: python

	import netports

	ports = netports.snumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
	print(ports)
	# 1 3 to 5


Interface4(line, splitter)
..........................

**Interface4** - An object of interface name, that can contain up to 4 indexes.
Sorts the interfaces by indexes (not by alphabetic).

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
line         	*str*						Interface name that can contain up to 4 indexes
splitter		*Iterable[str]*				Separator characters between indexes. By default ",./:"
=============== =========================== ============================================================================

Attributes demonstration

.. code:: python

	from netports import Interface4

	interface = Interface4("interface Ethernet1/2/3.4")
	assert interface.line == "interface Ethernet1/2/3.4"
	assert interface.name == "Ethernet1/2/3.4"
	assert interface.id0 == "interface Ethernet"
	assert interface.id1 == 1
	assert interface.id2 == 2
	assert interface.id3 == 3
	assert interface.id4 == 4

Interface with custom splitter between indexes. Splitter is ignored when comparing

.. code:: python

	from netports import Interface4

	interface1 = Interface4("interface Ethernet1/2/3.4")
	interface2 = Interface4("interface Ethernet1-2-3+4", splitter="-+")
	assert interface1 == interface2

Sorting by indexes

.. code:: python

	from netports import Interface4

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
	# interface Ethernet1/1/1.1
	# interface Ethernet1/2/1.1
	# interface Ethernet1/3/1.1
	# interface Ethernet1/20/1.1
	# interface Ethernet2/1/1.1
	# interface Ethernet10/1/1.1

Grouping interfaces by 3rd index

.. code:: python

	from netports import Interface4

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
	# interface Ethernet101/1/1
	# interface Ethernet102/1/1
	# interface Ethernet101/1/2
	# interface Ethernet102/1/2
	# interface Ethernet101/1/3
	# interface Ethernet102/1/3
