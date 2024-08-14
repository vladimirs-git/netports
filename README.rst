
.. image:: https://img.shields.io/pypi/v/netports.svg
   :target: https://pypi.python.org/pypi/netports
.. image:: https://img.shields.io/pypi/pyversions/netports.svg
   :target: https://pypi.python.org/pypi/netports


netports
========

Python tools for managing ranges of VLANs, TCP/UDP ports, IP protocols, Interfaces
Recommended for scripting in telecommunications networks.


Requirements
------------

Python >=3.8


Installation
------------

Install the package from pypi.org release

.. code:: bash

    pip install netports

or install the package from github.com release

.. code:: bash

    pip install https://github.com/vladimirs-git/netports/archive/refs/tags/0.14.0.tar.gz

or install the package from github.com repository

.. code:: bash

    pip install git+https://github.com/vladimirs-git/netports@0.14.0


.. contents:: **Contents**
    :local:


TCP/UDP ports
-------------

check_port()
............
**check_port(port, strict)**
Check TCP/UDP port in the range 1 to 65535.

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
port            *int*                       The TCP/UDP port that needs to be checked.
strict          *bool*                      True - raise NetportsValueError if the port is invalid, False - return False if the port is invalid. Default is `False`.
=============== =========================== ============================================================================

Return
    *bool* True - If the port is in the valid range of 1 to 65535, False - otherwise.
Raises
    *TypeError* If the port is not integer.
    *NetportsValueError* If strict=True and the port is outside the valid range.


check_port()
............
**check_ports(ports, strict)**
heck TCP/UDP ports in the range 1 to 65535.

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
ports           *List[int]*                 The TCP/UDP ports that needs to be checked
strict          *bool*                      True - raise NetportsValueError if any in the ports is invalid, False - return False if the port is invalid. Default is `False`.
=============== =========================== ============================================================================

Return
    *bool* True - if all ports is in the valid range of 1 to 65535, False - otherwise.
Raises
    *TypeError* If any in the ports is not integer.
    *NetportsValueError* If strict=True and any in the ports is outside the valid range.


itcp()
......
**itcp(items, verbose, all)**
Integer TCP/UDP Ports. Sorting TCP/UDP ports and removing duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of TCP/UDP ports, can be unsorted and with duplicates
verbose         *bool*                      True - all ports in verbose mode: [1, 2, ..., 65535], False - all ports in brief mode: [-1], to save RAM (default)
all             *bool*                      True - Returns all TCP/UDP ports: [1, 2, ..., 65535], or [-1] for verbose=False
=============== =========================== ============================================================================

Return
    *List[int]* of unique sorted TCP/UDP ports
Raises
    *NetportsValueError* if TCP/UDP ports are outside valid range 1...65535



stcp()
......
**stcp(items, verbose, all)**
String TCP/UDP ports. Sorting TCP/UDP ports and removing duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of TCP/UDP ports, can be unsorted and with duplicates
verbose         *bool*                      True - all ports in verbose mode: [1, 2, ..., 65535], False - all ports in brief mode: [-1], to save RAM (default)
all             *bool*                      True - Returns all TCP/UDP ports: "1-65535"
=============== =========================== ============================================================================

Return
    *str* of unique sorted TCP/UDP ports
Raises
    *NetportsValueError* if TCP/UDP ports are outside valid range 1...65535


**Examples**

`./examples/tcp_udp.py`_



VLAN IDs
--------


ivlan()
.......
**ivlan(items, verbose, all, splitter, range_splitter, platform)**
Sorting integer VLAN IDs and removing duplicates

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of VLANs, can be unsorted and with duplicates
verbose         *bool*                      True - all VLAN IDs in verbose mode: [1, 2, ..., 65535], False - all VLAN IDs in brief mode: [-1], to save RAM (default)
all             *bool*                      True - Returns all VLAN IDs: [1, 2, ..., 4094], or [-1] for verbose=False
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
platform        *str*                       Set ``splitter`` and ``range_splitter`` to platform specific values. Defined: "cisco" (Cisco IOS), "hpe" (Hewlett Packard Enterprise).
=============== =========================== ============================================================================

Return
    *List[int]* of unique sorted VLANs
Raises
    *NetportsValueError* if VLANs are outside valid range 1...4094


svlan()
.......
**svlan(items, verbose, all, splitter, range_splitter, platform)**
Sorting string VLANs and removing duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of VLANs, can be unsorted and with duplicates
verbose         *bool*                      True - all VLAN IDs in verbose mode: [1, 2, ..., 65535], False - all VLAN IDs in brief mode: [-1], to save RAM (default)
all             *bool*                      True - Returns all VLAN IDs: "1-4094"
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
platform        *str*                       Set ``splitter`` and ``range_splitter`` to platform specific values. Defined: "cisco" (Cisco IOS), "hpe" (Hewlett Packard Enterprise).
=============== =========================== ============================================================================

Return
    *str* of unique sorted VLANs
Raises
    *NetportsValueError* if VLANs are outside valid range 1...4094


**Examples**

`./examples/vlan.py`_



IP protocols
------------


IP_NAMES, IP_NUMBERS
....................

Dictionary with known IP protocol names and IDs listed in https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers


iip()
.....
**iip(items, verbose, all, strict)**
Sorting IP protocol numbers and removing duplicates


=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of IP protocol numbers, can be unsorted and with duplicates, "ip" - Return all IP protocol numbers: [0, 1, ..., 255]
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1], to save RAM (default)
strict          *bool*                      True - Raises NetportsValueError, if the protocol is unknown (default), False - Skips unknown protocols
all             *bool*                      True - Return all IP protocol numbers: [0, 1, ..., 255]
=============== =========================== ============================================================================

Return
    *List[int]* of unique sorted IP protocol numbers
Raises
    *NetportsValueError* if IP protocol numbers are outside valid range 0...255

sip()
.....
**sip(items, verbose, all)**
Soring string IP protocol numbers and removing duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of IP protocol numbers, can be unsorted and with duplicates. "ip" - mean all numbers in range 0...255.
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1], to save RAM (default)
strict          *bool*                      True - Raises NetportsValueError, if the protocol is unknown (default), False - Skips unknown protocols
all             *bool*                      True - Return all IP protocol numbers: "0-255"
=============== =========================== ============================================================================

Return
    *str* of unique sorted IP protocol numbers
Raises
    *NetportsValueError* if IP protocol numbers are outside valid range 0...255


ip_pairs()
..........
**ip_pairs(items, strict)**
Splits items to IP protocol Number, Name and undefined-invalid protocols

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of IP protocol names and numbers, can be unsorted and with duplicates
verbose         *bool*                      True - all protocols in verbose mode: [0, 1, ..., 255], False - all protocols in brief mode: [-1], to save RAM (default)
=============== =========================== ============================================================================

Return
    *List[Tuple[int, str]]* Pairs of IP protocol number and name,
     *List[str]* Undefined protocol names and invalid numbers


**Examples**

`./examples/ip.py`_



Objects
-------

Range()
.......
**Range(items, splitter, range_splitter, strict)**
An object that represents ports range as *str* and as *List[int]*
Object implements most of the `set <https://www.w3schools.com/python/python_ref_set.asp>`_ and
`list <https://www.w3schools.com/python/python_ref_list.asp>`_ methods that handle the Range.numbers attribute.

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str*, *List[int]*          Range of numbers. Numbers can be unsorted and duplicated.
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
strict          *bool*                      True - Raise NetportsValueError, if in items is invalid item. False - Make Range without invalid items. By default True.
=============== =========================== ============================================================================

Attributes demonstration


Range operators
:::::::::::::::

**Range** object implements:

- Arithmetic operators: ``+``, ``-``
- Reference to numbers in range by index

=============================== =========================== ============================================================
Operator                        Return                      Description
=============================== =========================== ============================================================
Range("1,4") + Range("3,5")     Range("1,3-5")              Add two objects
Range("1-5") - Range("2")       Range("1,3-5")              Subtract two objects
Range("1,3-5")[1]               3                           Get number by index
Range("1,3-5")[1:3]             [3, 4]                      Get numbers by slice
=============================== =========================== ============================================================


Range methods
:::::::::::::

**Range** object implements most of `set <https://www.w3schools.com/python/python_ref_set.asp>`_
and `list <https://www.w3schools.com/python/python_ref_list.asp>`_ methods.

=================================== ====================================================================================
Method                              Description
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


**Examples**

- Attributes demonstration
- Sorts numbers and removes duplicates
- Range with custom splitters

`./examples/range.py`_



Numbers
-------

parse_range()
.............
**parse_range(line, splitter, range_splitter)**
Parses range from line. Removes white spaces considering splitters.
Sort numbers and removes duplicates.

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
line            *str*                       Range of numbers, can be unsorted and with duplicates
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
    Range *object*


inumbers()
..........
**inumbers(items, splitter, range_splitter)**
Sort integer numbers and removes duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of numbers, can be unsorted and with duplicates
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
    *List[int]* of unique sorted numbers


snumbers()
..........
**snumbers(items, splitter, range_splitter)**
Sort string numbers and removes duplicates

=============== =========================== ============================================================================
Parameter       Type                        Description
=============== =========================== ============================================================================
items           *str, List[int], List[str]* Range of numbers, can be unsorted and with duplicates
splitter        *str*                       Separator character between items, by default ","
range_splitter  *str*                       Separator between min and max numbers in range, by default "-"
=============== =========================== ============================================================================

Return
    *str* of unique sorted numbers


**Examples**

- Sorts numbers and removes duplicates
- Range with custom splitter and range_splitter
- Converts unsorted range to sorted *List[int]* without duplicates
- Converts unsorted range to *List[int]* with custom splitters
- Converts unsorted range to sorted *str* without duplicates
- Converts unsorted range to *str* with custom splitters

`./examples/numbers.py`_


Interfaces
----------

intfrange()
...........
**intfrange(items, fmt)**
Convert interfaces names to shorted range notation

=========== ============ ===========================================================================
Parameter   Type         Description
=========== ============ ===========================================================================
items       *List[str]*  List of interfaces
fmt         *str*        Format option: "long"  - Long names: ["interface Ethernet1/1-3"], "short" - Short names: ["Eth1/1/1-3"]
=========== ============ ===========================================================================

Return
    *List[str]* Interface ranges


long_to_short()
...............
**long_to_short(device_type, key_lower, value_lower)**
Returns Interfaces map long-to-short, device_type specific

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
key_lower       *bool*                      True - keys lower-case, False - keys upper-case
value_lower     *bool*                      True - values lower-case, False - values upper-case
=============== =========================== ============================================================================

Return
    *Dict[str, str]* Interfaces map


long_to_long()
..............
**long_to_long(device_type, key_lower, value_lower)**
Returns Interfaces map long-to-long, device_type specific

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
key_lower       *bool*                      True - keys lower-case, False - keys upper-case
value_lower     *bool*                      True - values lower-case, False - values upper-case
=============== =========================== ============================================================================

Return
    *Dict[str, str]* Interfaces map


longs()
.......
**longs(device_type, value_lower)**
Returns long names of all interfaces

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
value_lower     *bool*                      True - values lower-case, False - values upper-case. Default is None, lower-case and upper-case.
=============== =========================== ============================================================================

Return
    *List[str]* Long names of all interfaces


short_to_long()
...............
**short_to_long(device_type, key_lower, value_lower)**
Returns Interfaces map short-to-long, device_type specific

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
key_lower       *bool*                      True - keys lower-case, False - keys upper-case
value_lower     *bool*                      True - values lower-case, False - values upper-case
=============== =========================== ============================================================================

Return
    *Dict[str, str]* Interfaces map


short_to_short()
................
**short_to_short(device_type, key_lower, value_lower)**
Returns Interfaces map short-to-short, device_type specific

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
key_lower       *bool*                      True - keys lower-case, False - keys upper-case
value_lower     *bool*                      True - values lower-case, False - values upper-case
=============== =========================== ============================================================================

Return
    *Dict[str, str]* Interfaces map


shorts()
........
**shorts(device_type, value_lower)**
Returns short names of all interfaces

=============== =========================== ============================================================================
Parameter        Type                        Description
=============== =========================== ============================================================================
device_type     *str*                       Netmiko device type
value_lower     *bool*                      True - values lower-case, False - values upper-case. Default is None, lower-case and upper-case.
=============== =========================== ============================================================================

Return
    *List[str]* Short names of all interfaces


Intf()
......
**Intf(line, device_type, splitter)**
An object of interface name, that can contain up to 4 indexes.
Sorts the interfaces by indexes (not by alphabetic).

=============== ======= ============================================================================
Parameter       Type    Description
=============== ======= ============================================================================
line            *str*   Interface name that can contain up to 4 indexes
device_type     *str*   Netmiko device_type (default "")
splitter        *str*   Separator of characters between indexes (default ",./:")
=============== ======= ============================================================================


Attributes
::::::::::

=============== ============ =======================================================================
Attributes      Type         Description
=============== ============ =======================================================================
delimiters                   Interface all delimiters
id0             *str*        Interface name. Line without IDs
id1             *int*        Interface 1st ID
id2             *int*        Interface 2nd ID
id3             *int*        Interface 3rd ID
id4             *int*        Interface 4th ID
ids                          Interface all IDs
line            *str*        Interface line
name            *str*        Interface name with IDs
splitter        *str*        Separator of characters between indexes
device_type     *str*        Netmiko device_type
=============== ============ =======================================================================


last_idx()
..........
**last_idx()**
Index of last ID in interface line


all_names()
...........
**all_names()**
All variants of names: long, short, upper-case, lover-case. Device type specific


name_full()
...........
**name_full()**
Interface long name with IDs and with interface keyword


name_long()
...........
**name_long()**
Interface long name with IDs and without interface keyword


name_short()
............
**name_short(replace)**
Interface short name with IDs, Device type specific

=========== =========================== ============================================================
Parameter   Type                        Description
=========== =========================== ============================================================
replace     *List[Tuple[str, str]]*     Replace the default short name with the first one
                                        that matches in the list of the `replace` argument.
=========== =========================== ============================================================

Return
    *str* Interface short name.


part_after()
............
**part_after(idx, splitter)**
Interface part after interested ID

=========== ============ ===========================================================================
Parameter   Type         Description
=========== ============ ===========================================================================
idx         *int*        Interface index
splitter    *bool*       True - Include splitter from edge, False - Skip splitter from edge
=========== ============ ===========================================================================

Return
    *str* Part of the interface name after specified interface index


part_before()
.............
**part_before(idx, splitter)**
Interface part before interested ID

=========== ============ ===========================================================================
Parameter   Type         Description
=========== ============ ===========================================================================
idx         *int*        Interface index
splitter    *bool*       True - Include splitter from edge, False - Skip splitter from edge
=========== ============ ===========================================================================

Return
    *str* Part of the interface name before specified interface index


**Examples**

- Attributes demonstration
- Interface with custom splitter between indexes. Splitter is ignored when comparing
- Sorting by indexes
- Grouping interfaces by 3rd index

`./examples/intfs.py`_


SwVersion()
...........
**SwVersion(text)**
Parse the given version string and return *SwVersion* object who can
compare (>, >=, <, <=) software versions of network devices: Cisco, FortiGate, HP, etc.


.. code:: python

    import re
    from netports import SwVersion

    text = "Cisco IOS Software, C2960X Software (C2960X-UNIVERSALK9-M), Version 15.2(4)E10, ..."
    text = re.search(r"Version (\S+),", text)[1]

    version1 = SwVersion(text)  # 15.2(4)E10
    version2 = SwVersion("15.2(4)E11")

    assert version1 < version2
    assert version1 <= version2
    assert not version1 > version2
    assert not version1 >= version2
    print(version1)  # 15.2(4)e10
    print(version2)  # 15.2(4)e11


.. _`./examples/tcp_udp.py` : ./examples/tcp_udp.py
.. _`./examples/vlan.py` : ./examples/vlan.py
.. _`./examples/ip.py` : ./examples/ip.py
.. _`./examples/range.py` : ./examples/range.py
.. _`./examples/numbers.py` : ./examples/numbers.py
.. _`./examples/intfs.py` : ./examples/intfs.py
