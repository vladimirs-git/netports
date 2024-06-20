"""Software Version"""
from typing import Tuple

from packaging.version import Version

from netports import helpers as h
from netports.types_ import TStrInt


class SwVersion(Version):
    """SwVersion"""

    def __init__(self, text: str):
        """SwVersion
        :param text: Cisco version text: "12.2(55)SE12"
        :type text: str
        """
        self._text = self._init_name(name=text)
        version, nano = self._parse_version(self._text)
        super().__init__(version)
        self._nano: int = nano

    # ========================== redefined ===========================

    def __repr__(self) -> str:
        name = self.__class__.__name__
        params = h.repr_params(self._text)
        return f"{name}({params})"

    def __str__(self) -> str:
        return self._text

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SwVersion):
            return False
        return self._text == other._text

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    # =========================== property ===========================

    @property
    def public(self) -> str:
        """Public version text"""
        return self._text

    @property
    def nano(self) -> int:
        """4th part of version
        :example:
            version = SwVersion("12.2(55)SE14")
            version.nano -> 14
        """
        return self._nano

    # =========================== helpers ============================

    @staticmethod
    def _init_name(**kwargs) -> str:
        """Init name"""
        name = kwargs.get("name")
        if name is None:
            name = ""
        if not name:
            name = "0"
        return str(name).lower()

    @staticmethod
    def _parse_version(text: str) -> TStrInt:
        """Init SwVersion. Split `text` to *Version* and `nano` (4th digit)"""
        nano = 0
        items = list(h.findall4(r"(\d+)\D+(\d+)\D+(\d+)\D+(\d+)", text))
        if items[3]:
            nano = int(items[3])
        else:
            items = list(h.findall3(r"(\d+)\D+(\d+)\D+(\d+)", text))
        if not items[0]:
            items = list(h.findall2(r"(\d+)\D+(\d+)", text))
            if not items[0]:
                if version := h.findall1(r"(\d+)", text):
                    items = [version]
                else:
                    items = []
        version = ".".join(items)
        if not version:
            version = "0"
        return version, nano
