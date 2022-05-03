"""Helper functions"""
from typing import Any

from netports.static import SPLITTER
from netports.types_ import LAny, LStr


def join(items: LAny) -> str:
    """Join items by "," """
    return SPLITTER.join([str(i) for i in items])


def list_of_str(items: Any) -> LStr:
    """Convert any types of items to *List[str]*"""
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


def split(items: Any) -> LStr:
    """Split items *str*, *List[str]* by "," and <space>"""
    results: LStr = []
    for items_s in list_of_str(items):
        for item_s in items_s.split():
            results.extend(item_s.split(SPLITTER))
    return results
