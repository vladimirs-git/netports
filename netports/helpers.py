"""Helper functions"""
from typing import Any

from netports.static import SPLITTER
from netports.types_ import LAny, LStr, StrInt, IStrInt, LInt


# =============================== str ================================

def join(items: LAny) -> str:
    """Joins items by "," """
    return SPLITTER.join([str(i) for i in items])


# =============================== list ===============================

def lstr(items: Any) -> LStr:
    """Converts any types of items to *List[str]*"""
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
    """Splits items *str*, *List[str]* by "," " " """
    results: LStr = []
    for items_s in lstr(items):
        for item_s in items_s.split():
            results.extend(item_s.split(SPLITTER))
    return results


# =============================== int ================================

def to_int(number: StrInt) -> int:
    """Converts *str* to *int*
    :param number: *int* or digit as *str*
    :return: *int*
    :raises TypeError: If number is not digit
    """
    if isinstance(number, int):
        return number
    if isinstance(number, str) and number.isdigit():
        return int(number)
    raise TypeError(f"{number=} {int} expected")


def to_lint(numbers: IStrInt) -> LInt:
    """Converts *List[str]* to *List[int]*
    :param numbers: *List[str]*
    :return: *List[int]*
    :raises TypeError: If number is not digit
    """
    if not isinstance(numbers, (list, set, tuple)):
        raise TypeError(f"{numbers=} {list} expected")
    return [to_int(s) for s in numbers]
