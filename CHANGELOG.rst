
.. :changelog:

CHANGELOG
=========

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
