"""IPv4 address representation in CIDR notation with host data under musk bits."""

from __future__ import annotations

from functools import total_ordering
from ipaddress import IPv4Interface, IPv4Network, IPv4Address
from typing import List

from vhelpers import vre

RE_IP = "\d+\.\d+\.\d+\.\d+"


@total_ordering
class IPv4:
    """IPv4 address representation in CIDR notation with host data under musk bits."""

    def __init__(self, cidr: str, strict: bool = False):
        """Initialize IPv4 object with the given CIDR notation.

        :param cidr: Address in CIDR notation with host data under musk bits.
        :param strict: If True, IP must be valid network address (not host address).
        :raises ValueError: If strict is True and a network address is not supplied.
        """
        self.interface = _init_cidr(cidr, strict)

    def __repr__(self):
        """Representation of the object."""
        return f"IPv4('{self.addr}')"

    def __str__(self):
        """String representation

        :return: IPv4 address with prefixlen, A.B.C.D/LEN.
        """
        return self.addr

    def __hash__(self) -> int:
        """Hash value of the object."""
        return hash(self.interface.network)

    def __eq__(self, other) -> bool:
        """Check if two objects are equal.

        :param other: Another object to compare.
        :return: True if objects are equal, False otherwise.
        """
        if not isinstance(other, IPv4):
            return False
        return self.interface == other.interface

    def __lt__(self, other) -> bool:
        """Compare two objects.

        :param other: Another object to compare with.
        """
        if not isinstance(other, IPv4):
            return False
        return self.interface < other.interface

    def __contains__(self, other: IPv4) -> bool:
        """Check if all IPs in the other subnet are part of this network."""
        return other.interface.network.subnet_of(self.interface.network)

    @property
    def addr(self) -> str:
        """IPv4 address with prefixlen, A.B.C.D/LEN."""
        return str(self.interface.with_prefixlen)

    @property
    def ip(self) -> str:
        """IPv4 address without prefixlen, A.B.C.D."""
        return str(self.interface.ip)

    @property
    def net(self) -> str:
        """IPv4 network with prefixlen, A.B.C.D/LEN."""
        return str(self.interface.network)

    @property
    def net_(self) -> str:
        """IPv4 network without prefixlen, A.B.C.D."""
        return str(self.interface.network.network_address)

    @property
    def prefixlen(self) -> int:
        """IPv4 network with prefixlen, A.B.C.D/LEN."""
        return self.interface.network.prefixlen

    # ================================ is ================================

    @property
    def is_global(self) -> bool:
        """True if the address is defined as globally reachable iana-ipv4-special-registry."""
        return bool(self.interface.ip.is_global)

    @property
    def is_link_local(self) -> bool:
        """True if the address is reserved for link-local usage. See RFC 3927."""
        return bool(self.interface.ip.is_link_local)

    @property
    def is_loopback(self) -> bool:
        """True if this is a loopback address. See RFC 3330."""
        return bool(self.interface.ip.is_loopback)

    @property
    def is_multicast(self) -> bool:
        """True if the address is reserved for multicast use. See RFC 3171."""
        return bool(self.interface.ip.is_multicast)

    @property
    def is_private(self) -> bool:
        """True if the address is defined as not globally reachable iana-ipv4-special-registry."""
        return bool(self.interface.ip.is_private)

    @property
    def is_reserved(self) -> bool:
        """True if the address is otherwise IETF reserved."""
        return bool(self.interface.ip.is_reserved)

    @property
    def is_unspecified(self) -> bool:
        """True if the address is unspecified. See RFC 5735."""
        return bool(self.interface.ip.is_unspecified)

    # ============================= objects ==============================

    @property
    def hostmask(self) -> IPv4Address:
        """The host mask, as an IPv4Address object."""
        return self.interface.hostmask

    @property
    def netmask(self) -> IPv4Address:
        """The net mask, as an IPv4Address object."""
        return self.interface.netmask

    @property
    def network(self) -> IPv4Network:
        """The network, as an IPv4Network object."""
        return self.interface.network

    # ============================== masks ===============================

    @property
    def addr_wildcard(self) -> str:
        """Address with the mask in wildcard mask notation, A.B.C.D 0.0.0.255."""
        return f"{self.interface.ip} {self.interface.hostmask}"

    @property
    def addr_mask(self) -> str:
        """Address with the mask in net mask notation, A.B.C.D 255.255.255.0."""
        return f"{self.interface.ip} {self.interface.netmask}"

    @property
    def net_wildcard(self) -> str:
        """Network with the mask in wildcard mask notation, A.B.C.D 0.0.0.255."""
        return f"{self.interface.network.network_address} {self.interface.network.hostmask}"

    @property
    def net_mask(self) -> str:
        """Network with the mask in net mask notation, A.B.C.D 255.255.255.0."""
        return f"{self.interface.network.network_address} {self.interface.network.netmask}"


LIPv4 = List[IPv4]


def _init_cidr(cidr: str, strict: bool) -> IPv4Interface:
    """Initialize a CIDR address, convert network with mask to A.B.C.D/LEN format.

    :param cidr: CIDR address or network with mask.
    :param strict: If True, IP must be valid network address (not host address).
    :return: IPv4Interface object representing the CIDR address.
    :raises ValueError: If strict is True and a network address is not supplied.
    """
    addr, mask = vre.find2(rf"({RE_IP})\D({RE_IP})", cidr)
    if addr and mask:
        network = IPv4Network(f"0.0.0.0/{mask}")
        prefixlen = network.prefixlen
        cidr = f"{addr}/{prefixlen}"
    if strict:
        IPv4Network(cidr, strict=strict)
    interface = IPv4Interface(cidr)
    return interface