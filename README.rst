netports
========

A collection of Python objects and functions for managing ranges of VLANs, TCP/UDP ports, interfaces.
Recommended for scripting related to telecommunications networks.

.. contents::

.. sectnum::


Installation
------------

Install the package by running

.. code:: bash

    pip install netports

or

.. code:: bash

    pip install git+https://github.com/vladimirs-git/netports


Objects
-------

Interface4(line)
................

**Interface4** - An object of interface name, that can contain up to 4 indexes.
Useful for sorting interface strings by index (not by alphabetic).

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
line         	*str*						Interface name that can contain up to 4 indexes.
splitter		*Iterable[str]*				Separator characters between indexes. By default ",./:".
=============== =========================== ============================================================================

Attributes demonstration.

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

Interface with custom splitter between indexes. Splitter is ignored when comparing.

.. code:: python

	from netports import Interface4

	interface1 = Interface4("interface Ethernet1/2/3.4")
	interface2 = Interface4("interface Ethernet1-2-3+4", splitter="-+")
	assert interface1 == interface2

Sorting by indexes.

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

	# Alphabetical sorting. This approach is not convenient in scripting.
	for line in sorted(lines):
		print(line)
	print()
	# interface Ethernet1/1/1.1
	# interface Ethernet1/2/1.1
	# interface Ethernet1/20/1.1
	# interface Ethernet1/3/1.1
	# interface Ethernet10/1/1.1
	# interface Ethernet2/1/1.1

	# Sorting by indexes. This approach is useful in scripting.
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

Grouping interfaces by 3rd index.

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
	print()
	# interface Ethernet101/1/1
	# interface Ethernet102/1/1
	# interface Ethernet101/1/2
	# interface Ethernet102/1/2
	# interface Ethernet101/1/3
	# interface Ethernet102/1/3


Ranges(line, splitter, range_splitter)
......................................

**Ranges** - An object that converts ``line`` numbers to *object* that represents range as *str* and as *List[int]*.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
line         	*str*						Range of numbers. Numbers can be unsorted and duplicated.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
strict			*bool*						True - Raise ValueError, if in line is invalid item. False - Make Range without invalid items. By default True.
=============== =========================== ============================================================================

Attributes demonstration.

.. code:: python

	ranges = Ranges("1,3-5")
	assert ranges.line == "1,3-5"
	assert ranges.numbers == [1, 3, 4, 5]

	try:
		Ranges("1,3-5,typo")
	except ValueError as ex:
		print(ex)
	# invalid item="typo" in line="1,3-5,typo"

	# Make Range without invalid items (by default raise ValueError)
	ranges = Ranges("1,3-5,typo,-1,1-", strict=False)
	assert ranges.line == "1,3-5"
	assert ranges.numbers == [1, 3, 4, 5]

Sorting numbers and removing duplicates.

.. code:: python

	from netports import Ranges

	ranges1 = Ranges("3-5,1")
	print(ranges1)
	# 1,3-5

	ranges2 = Ranges("3-5,1,3-5,1,3-4,4-5")
	print(ranges2)
	# 1,3-5

	assert ranges1 == ranges2


Range with custom splitters.

.. code:: python

	from netports import Ranges

	ranges = Ranges("1, 3-5, 7-9", splitter=", ")
	assert ranges.line == "1, 3-5, 7-9"
	assert ranges.numbers == [1, 3, 4, 5, 7, 8, 9]

	ranges = Ranges("1 3 to 5 7 to 9", splitter=" ", range_splitter=" to ")
	assert ranges.line == "1 3 to 5 7 to 9"
	assert ranges.numbers == [1, 3, 4, 5, 7, 8, 9]


Numbers
-------

ranges(line, splitter, range_splitter)
......................................

**range of numbers** - Sort numbers and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
line         	*str*						Range of numbers, can be unsorted and with duplicates.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
=============== =========================== ============================================================================

Return
	Ranges *object*.

Sort numbers and remove duplicates.

.. code:: python

	import netports

	ranges = netports.ranges("3-5,1,3-5,1")
	print(f"{ranges!r}")
	print(ranges.line)
	print(ranges.ports)
	print()
	# Ranges("1,3-5")
	# 1,3-5
	# [1, 3, 4, 5]

Range with custom splitter and range_splitter.

.. code:: python

	import netports

	ranges = netports.ranges("1 3 to 5 1 3 to 5", splitter=" ", range_splitter=" to ")
	print(f"{ranges!r}")
	print(ranges.line)
	print(ranges.ports)
	print()
	# Ranges("1 3 to 5", splitter=" ", range_splitter=" to ")
	# 1 3 to 5
	# [1, 3, 4, 5]


inumbers(items, splitter, range_splitter)
.........................................

**integer ports** - Sort numbers and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of numbers or *List[int]*, can be unsorted and with duplicates.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted numbers.

Convert unsorted range to sorted *List[int]* without duplicates.

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

Convert unsorted range to *List[int]* with custom splitters.

.. code:: python

	import netports

	ports = netports.inumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
	print(ports)
	# [1, 3, 4, 5]


snumbers(items, splitter, range_splitter)
.........................................

**string ports** - Sort numbers and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of numbers or *List[int]*, can be unsorted and with duplicates.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
=============== =========================== ============================================================================

Return
	*str* of unique sorted numbers.

Convert unsorted range to sorted *str* without duplicates.

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

Convert unsorted range to *str* with custom splitters.

.. code:: python

	import netports

	ports = netports.snumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
	print(ports)
	# 1 3 to 5


TCP/UDP ports
-------------


itcp(items)
...........

**Integer TCP/UDP ports** - Sort TCP/UDP ports and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates.
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted TCP/UDP ports.
	Raise *ValueError* if TCP/UDP ports are outside valid range 1...65535.

.. code:: python

	import netports

	ports = netports.itcp("80,20-21,80,20-21,20")
	print(ports)
	# [20, 21, 80]

	ports = netports.itcp(["80,20-21", "80", "20"])
	print(ports)
	# [20, 21, 80]

	ports = netports.itcp([80, 20, 21, 80, 20, 21])
	print(ports)
	# [20, 21, 80]

	try:
		netports.itcp("65536")
	except ValueError as ex:
		print(ex)
	# invalid_port=[65536], expected in range 1...65535


itcp_all()
..........

**All Integer TCP/UDP ports** - Full range of TCP/UDP ports.

Return
	*List[int]* All TCP/UDP ports.

.. code:: python

	import netports

	ports = netports.itcp_all()
	print(ports)
	# [1, 2, ..., 65535]


stcp(items)
...........

**String TCP/UDP ports** - Sort TCP/UDP ports and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates.
=============== =========================== ============================================================================

Return
	*str* of unique sorted TCP/UDP ports.
	Raise *ValueError* if TCP/UDP ports are outside valid range 1...65535.

.. code:: python

	import netports

	ports = netports.stcp("80,20-21,80,20-21,20")
	print(ports)
	# 20-21,80

	ports = netports.stcp(["80,20-21", "80", "20"])
	print(ports)
	# 20-21,80

	ports = netports.stcp([80, 20, 21, 80, 20, 21])
	print(ports)
	# 20-21,80

	try:
		netports.stcp("65536")
	except ValueError as ex:
		print(ex)
	# invalid_port=[65536], expected in range 1...65535




stcp_all()
..........

**All String TCP/UDP ports** - Full range of TCP/UDP ports.

Return
	*str* All TCP/UDP ports.

.. code:: python

	import netports

	ports = netports.stcp_all()
	print(ports)
	# 1-65535


VLAN IDs
--------


ivlan(line, splitter, range_splitter)
.....................................

**Integer VLAN IDs** - Sort VLANs and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs or *List[int]*, can be unsorted and with duplicates.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted VLANs.
	Raise *ValueError* if VLANs are outside valid range 1...4094.

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

	vlans = netports.ivlan(["1", "3-5", "3-4", "4-5"])
	print(vlans)
	# [1, 3, 4, 5]

	vlans = netports.ivlan([1, 1, 3, 3, 4, 4, 5, 5])
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


ivlan_all()
...........

**All Integer VLAN IDs** - Full range of VLAN IDs.

Return
	*List[int]* All VLAN IDs.

.. code:: python

	import netports

	ports = netports.ivlan_all()
	print(ports)
	# [1, 2, ..., 4094]


ivlan_hpe(items)
................

**Integer VLAN IDs, for Hewlett Packard Enterprise** - Sort VLANs and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs or *List[int]*, can be unsorted and with duplicates.
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted VLANs, for Hewlett Packard Enterprise.
	Raise *ValueError* if VLANs are outside valid range 1...4094.

.. code:: python

	import re
	import netports

	config = """
	interface Bridge-Aggregation1
	 port link-type hybrid
	 port hybrid vlan 1 3 to 5 tagged
	"""
	trunk = re.findall("vlan(.+)tagged", config)[0]  # " 1 3 to 5 "
	vlans = netports.ivlan_hpe(trunk)
	print(vlans)
	# [1, 3, 4, 5]

	vlans = netports.ivlan_hpe(["1", "3 to 5", "3 to 4", "4 to 5"])
	print(vlans)
	# [1, 3, 4, 5]

	vlans = netports.ivlan_hpe([1, 1, 3, 3, 4, 4, 5, 5])
	print(vlans)
	# [1, 3, 4, 5]

	try:
		netports.ivlan_hpe("4095")
	except ValueError as ex:
		print(ex)
	# invalid_vlan=[4095], expected in range 1...4094


svlan(line, splitter, range_splitter)
.....................................

**String VLAN IDs** - Sort VLANs and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs or *List[int]*, can be unsorted and with duplicates.
splitter     	*str*						Separator character between items. By default ",".
range_splitter	*str*						Separator between min and max numbers in range. By default "-".
=============== =========================== ============================================================================

Return
	*str* of unique sorted VLANs.
	Raise *ValueError* if VLANs are outside valid range 1...4094.

.. code:: python

	import netports

	vlans = netports.svlan("1,3-5,3-4,4-5")
	print(vlans)
	# 1,3-5

	vlans = netports.svlan(["1", "3-5", "3-4", "4-5"])
	print(vlans)
	# 1,3-5

	vlans = netports.svlan([1, 3, 4, 5])
	print(vlans)
	# 1,3-5

	vlans = netports.svlan("1 3 to 5", splitter=" ", range_splitter=" to ")
	print(vlans)
	# 1 3 to 5

	try:
		netports.svlan("4095")
	except ValueError as ex:
		print(ex)
	# invalid_vlan=[4095], expected in range 1...4094


svlan_all()
...........

**All String VLAN IDs** - Full range of VLAN IDs.

Return
	*str* All VLAN IDs.

.. code:: python

	import netports

	ports = netports.svlan_all()
	print(ports)
	# 1-4094


svlan_hpe(items)
................

**String VLAN IDs, for Hewlett Packard Enterprise** - Sort VLANs and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of VLANs or *List[int]*, can be unsorted and with duplicates.
=============== =========================== ============================================================================

Return
	*str* of unique sorted VLANs, for Hewlett Packard Enterprise.
	Raise *ValueError* if VLANs are outside valid range 1...4094.

.. code:: python

	import netports

	vlans = netports.svlan_hpe("1 3 to 5 3 to 4 4 to 5")
	print(vlans)
	# 1 3 to 5

	vlans = netports.svlan_hpe(["1", "3 to 5", "3 to 4", "4 to 5"])
	print(vlans)
	# 1 3 to 5

	vlans = netports.svlan_hpe([1, 3, 4, 5])
	print(vlans)
	# 1 3 to 5

	try:
		netports.svlan_hpe("4095")
	except ValueError as ex:
		print(ex)
	# invalid_vlan=[4095], expected in range 1...4094



IP protocols
------------


IP_NAMES, IP_PORTS
..................

Dictionary with known IP protocol names and ports (defined on https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers)


.. code:: python

	import netports

	print(netports.IP_NAMES)
	# {"icmp": {"number": 1, "name": "icmp"},
	#  "tcp": {"number": 6, "name": "tcp"},
	#  "udp": {"number": 17, "name": "udp"},
	#  ...
	# }

	print(netports.IP_PORTS)
	# {1: {"number": 1, "name": "icmp"},
	#  6: {"number": 6, "name": "tcp"},
	#  17: {"number": 17, "name": "udp"},
	#  ...
	# }


iip(items)
..........

**Integer IP protocol numbers** - Sort numbers and remove duplicates.


=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol numbers or *List[int]*, can be unsorted and with duplicates. "ip" - mean all numbers in range 0...255.
=============== =========================== ============================================================================

Return
	*List[int]* of unique sorted IP protocol numbers.
	Raise *ValueError* if IP protocol numbers are outside valid range 0...255.

.. code:: python

	import netports

	ports = netports.iip("icmp,tcp,7,255")
	print(ports)
	# [1, 6, 7, 255]

	ports = netports.iip(["icmp", "icmp,tcp,1", "6-7", "255"])
	print(ports)
	# [1, 6, 7, 255]

	ports = netports.iip([17, 17, 1, 1])
	print(ports)
	# [1, 17]

	try:
		netports.iip("265")
	except ValueError as ex:
		print(ex)
	# invalid_ip_numbers=[265], expected in range 0...255


iip_all()
.........

**All Integer IP protocol numbers** - Full range of IP protocol numbers.

Return
	*List[int]* All IP protocol numbers.

.. code:: python

	import netports

	ports = netports.iip_all()
	print(ports)
	# [1, 2, ..., 255]


iip_nip(items)
..............

**IP protocol Numbers and Names** - Split numbers and names and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol numbers and names, can be unsorted and with duplicates.
=============== =========================== ============================================================================

Return
	List of IP protocol Numbers and List of IP protocol Names.
	Raise *ValueError* if IP protocol number are outside valid range 0...255.
	Raise *ValueError* if IP protocol name is unknown.

.. code:: python

	import netports

	ports = netports.iip_nip("icmp,tcp,7,255")
	print(ports)
	# ([7, 255], ["icmp", "tcp"])

	ports = netports.iip_nip(["icmp", "tcp", 7, 255])
	print(ports)
	# ([7, 255], ["icmp", "tcp"])


	try:
		netports.iip_nip("icmp,typo")
	except ValueError as ex:
		print(ex)
	# invalid_ip_names=["typo"]


sip(items)
..........

**String IP protocol numbers** - Sort numbers and remove duplicates.

=============== =========================== ============================================================================
Parameter		Type						Description
=============== =========================== ============================================================================
items         	*str, List[int], List[str]*	Range of IP protocol numbers or *List[int]*, can be unsorted and with duplicates. "ip" - mean all numbers in range 0...255.
=============== =========================== ============================================================================

Return
	*str* of unique sorted IP protocol numbers.
	Raise *ValueError* if IP protocol numbers are outside valid range 0...255.

.. code:: python

	import netports

	ports = netports.sip("icmp,tcp,7,255")
	print(ports)
	# 1,6-7,255

	ports = netports.sip(["icmp", "icmp,tcp,1", "6-7", "255"])
	print(ports)
	# 1,6-7,255

	ports = netports.sip([255, 255, 1, 1, 6, 7])
	print(ports)
	# 1,6-7,255

	try:
		netports.sip("265")
	except ValueError as ex:
		print(ex)
	# invalid_ip_numbers=[265], expected in range 0...255


sip_all()
.........

**All String IP protocol numbers** - Full range of IP protocol numbers.

Return
	*str* All IP protocol numbers.

.. code:: python

	import netports

	ports = netports.sip_all()
	print(ports)
	# 0-255


