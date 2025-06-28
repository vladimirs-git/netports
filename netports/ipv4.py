"""IPv4 address representation in CIDR notation with host data under mask bits."""

from __future__ import annotations

import re
from functools import total_ordering
from ipaddress import IPv4Interface, IPv4Network, IPv4Address
from typing import List

from pydantic import BaseModel, Field
from vhelpers import vre

RE_IP = "\d+\.\d+\.\d+\.\d+"


@total_ordering
class IPv4(BaseModel):
    """IPv4 address representation in CIDR notation with host data under mask bits."""

    addr: str = Field(description="IPv4 address with host data under mask bits. A.B.C.D/LEN")
    ip: str = Field(default="", description="IPv4 address without prefixlen, A.B.C.D")
    prefix: str = Field(default="", description="IPv4 prefix without host data, A.B.C.D/LEN")
    len: int = Field(default="", description="Prefix length")

    def __init__(self, *args, **kwargs):
        """Initialize IPv4 object with the given CIDR notation.

        :param addr: IP address in CIDR notation with host data under mask bits.
        :param strict: If True, IP must be valid network address (not host address).
        :raises ValueError: If the CIDR address is invalid
            or cannot be converted from network with mask format.
        """
        addr: str = _validate_addr(*args, **kwargs)
        super().__init__(addr=addr)
        self._interface = IPv4Interface(address=addr)
        self.ip = str(self._interface.ip)
        self.prefix = str(self._interface.network)
        self.len = int(self._interface.network.prefixlen)

    def __repr__(self) -> str:
        """Representation of the object."""
        class_ = self.__class__.__name__
        return f"{class_}('{self.addr}')"

    def __str__(self):
        """String representation.

        :return: IPv4 address with prefixlen, A.B.C.D/LEN.
        """
        return self.addr

    def __hash__(self) -> int:
        """Hash value of the object."""
        return hash(self._interface.network)

    def __eq__(self, other) -> bool:
        """Check if two objects are equal.

        :param other: Another object to compare.
        :return: True if objects are equal, False otherwise.
        """
        if not isinstance(other, IPv4):
            return False
        return self._interface == other._interface

    def __lt__(self, other) -> bool:
        """Compare two objects.

        :param other: Another object to compare with.
        """
        if not isinstance(other, IPv4):
            return False
        return self._interface < other._interface

    def __contains__(self, other: IPv4) -> bool:
        """Check if all IPs in the other subnet are part of this network."""
        return other._interface.network.subnet_of(self._interface.network)

    # ================================ is ================================

    def is_address(self) -> bool:
        """True if the address with host data under mask bits, False if the prefix."""
        if self.len == 32:
            return True
        try:
            IPv4Network(self.addr, strict=True)
        except ValueError:
            return True
        return False

    def is_prefix(self) -> bool:
        """True if the prefix without host data under mask bits, False if the address."""
        return not self.is_address()

    def is_global(self) -> bool:
        """True if the address is defined as globally reachable iana-ipv4-special-registry."""
        return bool(self._interface.ip.is_global)

    def is_link_local(self) -> bool:
        """True if the address is reserved for link-local usage. See RFC 3927."""
        return bool(self._interface.ip.is_link_local)

    def is_loopback(self) -> bool:
        """True if this is a loopback address. See RFC 3330."""
        return bool(self._interface.ip.is_loopback)

    def is_multicast(self) -> bool:
        """True if the address is reserved for multicast use. See RFC 3171."""
        return bool(self._interface.ip.is_multicast)

    def is_private(self) -> bool:
        """True if the address is defined as not globally reachable iana-ipv4-special-registry."""
        return bool(self._interface.ip.is_private)

    def is_reserved(self) -> bool:
        """True if the address is otherwise IETF reserved."""
        return bool(self._interface.ip.is_reserved)

    def is_unspecified(self) -> bool:
        """True if the address is unspecified. See RFC 5735."""
        return bool(self._interface.ip.is_unspecified)

    # ============================= objects ==============================

    def hostmask(self) -> IPv4Address:
        """The host mask, as an IPv4Address object."""
        return self._interface.hostmask

    def netmask(self) -> IPv4Address:
        """The net mask, as an IPv4Address object."""
        return self._interface.netmask

    def network(self) -> IPv4Network:
        """The network, as an IPv4Network object."""
        return self._interface.network

    # ============================== masks ===============================

    def addr_mask(self, splitter: str = " ") -> str:
        """Address with the mask in net mask notation, A.B.C.D 255.255.255.0.

        :param splitter: String to split network address and hostmask.
        :return: Address with hostmask in net mask notation.
        """
        return f"{self._interface.ip}{splitter}{self._interface.netmask}"

    def addr_wildcard(self, splitter: str = " ") -> str:
        """Address with the mask in wildcard mask notation, A.B.C.D 0.0.0.255.

        :param splitter: String to split network address and hostmask.
        :return: Address with hostmask in wildcard mask notation.
        """
        return f"{self._interface.ip}{splitter}{self._interface.hostmask}"

    def net_mask(self, splitter: str = " ") -> str:
        """Network with the mask in net mask notation, A.B.C.D 255.255.255.0.

        :param splitter: String to split network address and hostmask.
        :return: Network address with hostmask in net mask notation.
        """
        network_address = self._interface.network.network_address
        netmask = self._interface.network.netmask
        return f"{network_address}{splitter}{netmask}"

    def net(self) -> str:
        """Network without prefixlen, A.B.C.D."""
        return str(self._interface.network.network_address)

    def net_wildcard(self, splitter: str = " ") -> str:
        """Network with the mask in wildcard mask notation, A.B.C.D 0.0.0.255.

        :param splitter: String to split network address and hostmask.
        :return: Network address with hostmask in wildcard mask notation.
        """
        network_address = self._interface.network.network_address
        hostmask = self._interface.network.hostmask
        return f"{network_address}{splitter}{hostmask}"


LIPv4 = List[IPv4]


def _validate_addr(*args, **kwargs) -> str:
    """Validate IPv4 address, convert address or network with mask to CIDR A.B.C.D/LEN format.

    :param args: Arguments containing the address value.
    :param addr: IP address in CIDR notation with host data under mask bits.
    :param strict: If True, IP must be valid network address (not host address).
    :return: IPv4 address representation in CIDR notation with host data under mask bits.
    :raises ValueError: If the address is invalid or cannot be converted from network/mask format.
    """
    addr = ""
    if args:
        addr = args[0]
    if not addr:
        addr = str(kwargs.get("addr") or "")
    addr = addr.strip()

    strict = bool(kwargs.get("strict"))

    # addr
    if re.search(rf"^{RE_IP}/\d+$", addr):
        pass
    elif re.search(rf"^{RE_IP}$", addr):
        addr = f"{addr}/32"
    else:
        prefix, mask = vre.find2(rf"^({RE_IP})\D({RE_IP})$", addr)
        if not (prefix and mask):
            raise ValueError(f"Invalid address format")
        network = IPv4Network(f"0.0.0.0/{mask}")
        prefixlen = network.prefixlen
        addr = f"{prefix}/{prefixlen}"

    _ = IPv4Network(addr, strict=strict)
    return addr
