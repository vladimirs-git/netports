
.. :changelog:

CHANGELOG
=========

0.13.2 (2024-07-18)
-------------------
* [change] intf_map.MAP_CISCO_IOS AppGigabitEthernet


0.13.0 (2024-07-13)
-------------------
* [new] intf_map.shorts() intf_map.longs()
* [new] Intf.name_base()
* [add] intf_map HundredGigE
* [delete] intf_map FortyGigabitEthernet


0.12.2 (2024-06-20)
-------------------
* [fix] version="" > version="0"


0.12.1 (2023-12-05)
-------------------
* [fix] dependency packaging


0.12.0 (2023-12-05)
-------------------
* [change] poetry


0.11.1 (2023-12-03)
-------------------
* [new] check_port() check_ports()


0.10.0 (2023-11-03)
-------------------
* [new] SwVersion()


0.9.0 (2023-10-23)
------------------
* [new] intf_map.py ALL_SHORT
* [change] platform > device_type
* [change] Intf._init_device_type() ValueError > NetportsValueError
* [new] Intf.name_short(replace=[("Fa", "Eth")])

0.8.2 (2023-04-04)
------------------
* [change] Intf(platform="hp_procurve").all_names() -> ["interface Trk1", ...]

0.8.1 (2023-04-04)
------------------
* [change] Intf(platform="hp_procurve").all_names() -> ["interface 1", "1", "interface 1/1"]


0.8.0 (2023-04-03)
------------------
* [delete] Intf.part()
* [new] Intf.part_after()
* [new] Intf.part_before()
* [change] Intf.name_short > Intf.name_short(), property changed to method
* [change] ValueError > NetportsValueError
* [new] intf_map.short_to_long() intf_map.long_to_short()


0.7.3 (2023-01-24)
------------------
* [fix] Intf.all_names() > mgmt0


0.7.2 (2022-12-17)
------------------
* [fix] Intf.all_names() for HP Procurve


0.7.1 (2022-12-06)
------------------
* [change] Intf.names() to Intf.all_names()
* [new] intf_name_map.py short_to_long, short_to_long_lower


0.7.0 (2022-12-05)
------------------
* [new] Intf.names()
* [change] Intf.name_short


0.6.2 (2022-11-14)
------------------
* [change] pyproject.toml
* [change] vlan.py check_vlans()
* [change] tcp.py check_tcp_ports()

0.6.1 (2022-11-01)
------------------
* [fix] py.typed


0.6.0 (2022-11-01)
------------------
* [rename] Interface4 > Intf
* [new] IntfGM
* [new] pyproject.toml


0.5.2 (2022-07-30)
------------------
* [new] netports.ip_pairs(items, strict)
* [chang] param is_verbose, by default True
* [new] ip.py IP_ALIASES


0.5.0 (2022-06-19)
------------------
* [new] param `verbose` in functions: itcp, stcp, ivlan, svlan, iip, sip


0.4.0 (2022-06-18)
------------------
* [change] netports.IP_PORTS to netports.IP_NUMBERS
* [change] netports.Range._items to netports.Range.items
* [new] iip(strict)


0.3.0 (2022-05-16)
------------------
* [change] Range.numbers. The *numbers* property has been changed to the method, because a full set of ports takes up a lot of RAM.


0.2.0 (2022-05-12)
------------------
* [new] itcp(all=True), stcp(all=True), ivlan(all=True), svlan(all=True), iip, nip, sip
* [change] Ranges.ports > Ranges.numbers
* arithmetic, list, set methods for Ranges


0.1.1 (2022-05-02)
------------------
* [fix] setup.py README.rst


0.1.0 (2022-05-02)
------------------
* Development Status :: 5 - Production/Stable
