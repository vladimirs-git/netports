"""Helper functions"""
from typing import Any

from netports.types_ import LStr


def list_of_str(items: Any) -> LStr:
    """Convert any types of items to list of string"""
    if not isinstance(items, (bytes, dict, float, int, list, set, str, tuple)):
        raise TypeError(f"{items=} {list} expected")
    if isinstance(items, (bytes, float, int, str)):
        items = [items]
    items_ = []
    for item in items:
        if isinstance(item, bytes):
            items_.append(item.decode("utf-8"))
        elif isinstance(item, float):
            items_.append(str(int(item)))
        else:
            items_.append(str(item))
    return items_
