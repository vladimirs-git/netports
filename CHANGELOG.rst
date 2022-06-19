
.. :changelog:

CHANGELOG
=========

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
