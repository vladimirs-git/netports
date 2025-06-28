"""MAC address representation in different formats."""

from __future__ import annotations

import string
from functools import total_ordering
from typing import List, Optional, Set, Tuple, Union

from pydantic import BaseModel, Field

from netports.exceptions import NetportsValueError
from netports.types_ import LStr


@total_ordering
class Mac(BaseModel):
    """MAC address representation in different formats."""

    addr: str = Field(description="MAC address")
    hex: str = Field(description="MAC address as 12-character hexadecimal string")
    integer: int = Field(description="MAC address as integer")

    def __init__(self, *args, **kwargs):
        """Initialize Mac.

        :param line: MAC address line.
        """
        addr = _validate_addr(*args, **kwargs)
        hex_ = _validate_hex(addr)
        integer = int(hex_, 16)
        super().__init__(addr=addr, hex=hex_, integer=integer)

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
        chunks = [self.hex[i:i + size] for i in range(0, 12, size)]
        return splitter.join(chunks)

    def cisco(self) -> str:
        """Return MAC in Cisco dot format: 0000.0000.0000."""
        addr = self.format(size=4, splitter=".")
        return addr.lower()

    def hp_comware(self) -> str:
        """Return MAC in hp_comware dash format: 0000-0000-0000."""
        addr = self.format(size=4, splitter="-")
        return addr.lower()

    def hp_procurve(self) -> str:
        """Return MAC in hp_procurve dash format: 000000-000000."""
        addr = self.format(size=6, splitter="-")
        return addr.lower()

    def linux(self) -> str:
        """Return MAC in Linux colon format: 00:00:00:00:00:00."""
        addr = self.format(size=2, splitter=":")
        return addr.lower()

    def windows(self) -> str:
        """Return MAC in Windows dash format: 00-00-00-00-00-00."""
        addr = self.format(size=2, splitter="-")
        return addr.lower()


LMac = List[Mac]
SMac = Set[Mac]
TMac = Tuple[Mac]
ULMac = Optional[Union[str, LStr, Mac, LMac]]


# ============================= helpers ==============================


def _validate_addr(*args, **kwargs) -> str:
    """Extract MAC address line from arguments or keyword arguments.

    :param args: Tuple of arguments.
    :param kwargs: Dictionary of keyword arguments.
    :return: MAC address as a string.
    """
    addr = ""
    if args:
        addr = str(args[0])
    if not addr:
        addr = str(kwargs.get("addr") or "")
    return addr.strip()


def _validate_hex(addr: str) -> str:
    """Convert MAC address to hex string.

    :param addr: MAC address as a string.
    :return: MAC address as a 12-character hex string.
    :raises NetportsValueError: If the line does not match the MAC address pattern.
    """
    # splitter
    expected = ":.-"
    splitter = set(addr).difference(set(expected))
    if splitter := splitter.difference(set(string.hexdigits)):
        raise NetportsValueError(f"Invalid {splitter=!r}, {expected=}.")

    # hex
    hexdigits: LStr = [s for s in addr if s in string.hexdigits]
    line = "".join(hexdigits)
    if len(line) != 12:
        raise NetportsValueError("12 hexdigits expected.")
    return "".join(hexdigits)
