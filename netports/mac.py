"""An object representing a MAC address in different formats."""

from __future__ import annotations

import string
from functools import total_ordering
from typing import List, Optional, Set, Tuple, Union

from pydantic import BaseModel, Field

from netports.exceptions import NetportsValueError
from netports.types_ import LStr


@total_ordering
class Mac(BaseModel):
    """An object representing a MAC address in different formats."""

    line: str = Field(description="MAC address line")
    hex: str = Field(default="", description="MAC address in hex format")
    cisco: str = Field(default="", description="MAC address in cisco_ios format")
    colon: str = Field(default="", description="MAC address in colon delimiter format")
    hp: str = Field(default="", description="MAC address in hp_procurve format")
    integer: int = Field(default=0, description="MAC address in integer format")

    def __init__(self, *args, **kwargs):
        """Init Mac.

        :param line: MAC address line.
        """
        line: str = _arg_line(*args, **kwargs)
        super().__init__(line=line)
        self._parse()

    def __str__(self):
        """__str__."""
        return self.line

    def __repr__(self):
        """__repr__."""
        name = self.__class__.__name__
        return f"{name}({self.line!r})"

    def __hash__(self) -> int:
        """__hash__."""
        return hash(self.integer)

    def __eq__(self, other) -> bool:
        """== equality."""
        if self.__class__ == other.__class__:
            if self.__hash__() == other.__hash__():
                return True
        return False

    def __lt__(self, other) -> bool:
        """< less than."""
        if self.__class__ == other.__class__:
            return self.integer < other.integer
        return False

    def __copy__(self) -> Mac:
        """Create a duplicate of the object.

        :return: A copy of the current object.
        """
        return type(self)(line=self.line)

    # ============================== parse ===============================

    def _parse(self) -> None:
        """Init MAC address with given value.

        :return: None. Update data in object.
        """
        self._parse_hex()
        self._parse_cisco()
        self._parse_hp()
        self._parse_colon()
        self._parse_integer()

    def _parse_hex(self) -> None:
        """Convert MAC address to hex string.

        :return: None. Update data in object.
        :raises NetportsValueError: If the line does not match the MAC address pattern.
        """
        # splitter
        expected = ":.-"
        splitter = set(self.line).difference(set(expected))
        if splitter := splitter.difference(set(string.hexdigits)):
            raise NetportsValueError(f"Invalid {splitter=!r}, {expected=}.")

        # hex
        hexdigits: LStr = [s for s in self.line.lower() if s in string.hexdigits]
        line = "".join(hexdigits)
        if len(line) != 12:
            raise NetportsValueError("12 hexdigits expected.")
        self.hex = "".join(hexdigits)

    def _parse_cisco(self) -> None:
        """Convert MAC address to cisco_ios format.

        :return: None. Update data in object.
        """
        items = [
            self.hex[:4],
            self.hex[4:8],
            self.hex[8:],
        ]
        self.cisco = ".".join(items)

    def _parse_hp(self) -> None:
        """Convert MAC address to hp_procurve format.

        :return: None. Update data in object.
        """
        items = [
            self.hex[:6],
            self.hex[6:],
        ]
        self.hp = "-".join(items)

    def _parse_colon(self) -> None:
        """Convert MAC address to colon delimiter format.

        :return: None. Update data in object.
        """
        items = [
            self.hex[:2],
            self.hex[2:4],
            self.hex[4:6],
            self.hex[6:8],
            self.hex[8:10],
            self.hex[10:],
        ]
        self.colon = ":".join(items)

    def _parse_integer(self) -> None:
        """Convert MAC address to integer format.

        :return: None. Update data in object.
        """
        self.integer = int(self.hex, 16)


LMac = List[Mac]
SMac = Set[Mac]
TMac = Tuple[Mac]
ULMac = Optional[Union[str, LStr, Mac, LMac]]


# ============================ functions =============================


def _arg_line(*args, **kwargs) -> str:
    """Extract MAC address line from arguments or keyword arguments.

    :param args: Tuple of arguments.
    :param kwargs: Dictionary of keyword arguments.
    :return: MAC address as a string.
    """
    line = ""
    if args:
        line = str(args[0])
    elif "line" in kwargs:
        line = str(kwargs["line"])
    return line
