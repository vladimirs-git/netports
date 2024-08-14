
.. :changelog:

CHANGELOG
=========

0.14.0 (2024-08-14)
-------------------

**Added:** intf.is_port_base()


0.13.2 (2024-07-18)
-------------------

**Changed:** intf_map.MAP_CISCO_IOS AppGigabitEthernet


0.13.0 (2024-07-13)
-------------------

**Added:** intf_map.shorts() intf_map.longs()

**Added:** Intf.name_base()

**Added:** intf_map HundredGigE

**Deleted:** intf_map FortyGigabitEthernet


0.12.2 (2024-06-20)
-------------------

**Fixed:** version="" > version="0"


0.12.1 (2023-12-05)
-------------------

**Fixed:** dependency packaging


0.12.0 (2023-12-05)
-------------------

**Changed:** poetry


0.11.1 (2023-12-03)
-------------------

**Added:** check_port() check_ports()


0.10.0 (2023-11-03)
-------------------

**Added:** SwVersion()


0.9.0 (2023-10-23)
------------------

**Added:** intf_map.py ALL_SHORT

**Changed:** platform > device_type

**Changed:** Intf._init_device_type() ValueError > NetportsValueError

**Added:** Intf.name_short(replace=[("Fa", "Eth")])


0.8.2 (2023-04-04)
------------------

**Changed:** Intf(platform="hp_procurve").all_names() -> ["interface Trk1", ...]


0.8.1 (2023-04-04)
------------------

**Changed:** Intf(platform="hp_procurve").all_names() -> ["interface 1", "1", "interface 1/1"]


0.8.0 (2023-04-03)
------------------

**Deleted:** Intf.part()

**Added:** Intf.part_after()

**Added:** Intf.part_before()

**Changed:** Intf.name_short > Intf.name_short(), property changed to method

**Changed:** ValueError > NetportsValueError

**Added:** intf_map.short_to_long() intf_map.long_to_short()


0.7.3 (2023-01-24)
------------------

**Fixed:** Intf.all_names() > mgmt0


0.7.2 (2022-12-17)
------------------

**Fixed:** Intf.all_names() for HP Procurve


0.7.1 (2022-12-06)
------------------

**Changed:** Intf.names() to Intf.all_names()

**Added:** intf_name_map.py short_to_long, short_to_long_lower


0.7.0 (2022-12-05)
------------------

**Added:** Intf.names()

**Changed:** Intf.name_short


0.6.2 (2022-11-14)
------------------

**Changed:** pyproject.toml

**Changed:** vlan.py check_vlans()

**Changed:** tcp.py check_tcp_ports()


0.6.1 (2022-11-01)
------------------

**Fixed:** py.typed


0.6.0 (2022-11-01)
------------------

**Changed:** Interface4 > Intf

**Added:** IntfGM

**Added:** pyproject.toml


0.5.2 (2022-07-30)
------------------

**Added:** netports.ip_pairs(items, strict)

**Changed:** param is_verbose, by default True

**Added:** ip.py IP_ALIASES


0.5.0 (2022-06-19)
------------------

**Added:** param `verbose` in functions: itcp, stcp, ivlan, svlan, iip, sip


0.4.0 (2022-06-18)
------------------

**Changed:** netports.IP_PORTS to netports.IP_NUMBERS

**Changed:** netports.Range._items to netports.Range.items

**Added:** iip(strict)


0.3.0 (2022-05-16)
------------------

**Changed:** Range.numbers. The *numbers* property has been changed to the method, because a full set of ports takes up a lot of RAM.


0.2.0 (2022-05-12)
------------------

**Added:** itcp(all=True), stcp(all=True), ivlan(all=True), svlan(all=True), iip, nip, sip

**Changed:** Ranges.ports > Ranges.numbers


0.1.1 (2022-05-02)
------------------

**Fixed:** setup.py README.rst
