"""MAC address representation in different formats."""

from __future__ import annotations

import string
from functools import total_ordering
from typing import List, Dict

from pydantic import BaseModel, Field

from netports.exceptions import NetportsValueError
from netports.types_ import LStr, T2Str


@total_ordering
class Mac(BaseModel):
    """MAC address representation in different formats."""

    addr: str = Field(description="MAC address")

    def __init__(self, *args, **kwargs):
        """Initialize Mac.

        :param addr: MAC address.
        :raises NetportsValueError: If the MAC address is invalid or empty.
        """
        addr, hex_ = _validate_addr(*args, **kwargs)
        kwargs_ = {k: v for k, v in kwargs.items() if k != "addr"}
        super().__init__(addr=addr, **kwargs_)
        self._hex = hex_

    def __repr__(self) -> str:
        """Representation of the object."""
        class_ = self.__class__.__name__
        return f"{class_}({self.addr!r})"

    def __str__(self) -> str:
        """String representation."""
        return str(self.addr)

    def __hash__(self) -> int:
        """Hash value of the object."""
        return hash(self.integer)

    def __eq__(self, other) -> bool:
        """Check if two objects are equal.

        :param other: Another object to compare.
        :return: True if objects are equal, False otherwise.
        """
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """Compare two objects.

        :param other: Another object to compare with.
        """
        if self.__class__ == other.__class__:
            return self.integer < other.integer
        return False

    def __copy__(self) -> Mac:
        """Create a duplicate of the object.

        :return: A copy of the current object.
        """
        return type(self)(line=self.addr)

    # ============================= property =============================

    @property
    def hex(self) -> str:
        """MAC address as 12-character hexadecimal string."""
        return self._hex

    @property
    def integer(self) -> int:
        """MAC address as integer."""
        return int(self.hex, 16)

    @property
    def cisco(self) -> str:
        """Return MAC in Cisco dot format: 0000.0000.0000."""
        addr = self.format(size=4, splitter=".")
        return addr.lower()

    @property
    def hp_comware(self) -> str:
        """Return MAC in hp_comware dash format: 0000-0000-0000."""
        addr = self.format(size=4, splitter="-")
        return addr.lower()

    @property
    def hp_procurve(self) -> str:
        """Return MAC in hp_procurve dash format: 000000-000000."""
        addr = self.format(size=6, splitter="-")
        return addr.lower()

    @property
    def linux(self) -> str:
        """Return MAC in Linux colon format: 00:00:00:00:00:00."""
        addr = self.format(size=2, splitter=":")
        return addr.lower()

    @property
    def windows(self) -> str:
        """Return MAC in Windows dash format: 00-00-00-00-00-00."""
        addr = self.format(size=2, splitter="-")
        return addr.lower()

    # ============================= methods ==============================

    def format(self, size: int, splitter: str) -> str:
        """Format MAC address, split into chunks of given size.

        :param size: Integer value to determine the grouping size.
        :param splitter: String to use as a separator.
        :return: Formatted string.
        :raises NetportsValueError: If invalid size.
        """
        if size not in [2, 4, 6]:
            raise NetportsValueError(f"Invalid {size=}")
        chunks = [self.hex[i : i + size] for i in range(0, 12, size)]
        return splitter.join(chunks)


LMac = List[Mac]
DMac = Dict[str, Mac]


# ============================= helpers ==============================


def _validate_addr(*args, **kwargs) -> T2Str:
    """Extract MAC address line from arguments or keyword arguments.

    :param args: Tuple of arguments.
    :param kwargs: Dictionary of keyword arguments.
    :return: MAC address as a string.
    """
    # addr
    addr = ""
    if args:
        addr = str(args[0])
    if not addr:
        addr = str(kwargs.get("addr") or "")
    if not addr:
        raise NetportsValueError("MAC address is empty.")

    # splitter
    expected = string.hexdigits + ":.-"
    if set(addr).difference(set(expected)):
        raise NetportsValueError("Invalid MAC address splitter")

    # hex
    hexdigits: LStr = [s for s in addr if s in string.hexdigits]
    line = "".join(hexdigits)
    if len(line) != 12:
        raise NetportsValueError("Invalid MAC address format, 12 hexdigits expected.")
    hex_ = "".join(hexdigits)

    return addr, hex_
