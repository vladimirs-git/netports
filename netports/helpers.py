"""Helper functions"""
import time
from typing import Any, Iterable

from netports.static import BRIEF_ALL_I, BRIEF_ALL_S, SPLITTER
from netports.types_ import LAny, LStr, StrInt, IStrInt, LInt


# =============================== bool ===============================

def is_all(**kwargs) -> bool:
    """Get param `all` from `kwargs`"""
    return bool(kwargs.get("all"))


def is_brief(**kwargs) -> bool:
    """Get param `verbose` from `kwargs` and reverse the result"""
    return not is_verbose(**kwargs)


def is_brief_all(items: Any) -> bool:
    """Checks is "-1" or -1 in `items`, used for verbose=False
    :param items: *str, int, List[str], List[int]*
    :return: True - if "-1" or -1 present in `items`
    """
    if isinstance(items, (str, int)):
        items = [items]
    if not isinstance(items, Iterable):
        raise TypeError(f"{items=} expected {str}")
    for item in items:
        if isinstance(item, str):
            if item == BRIEF_ALL_S:
                return True
            continue
        if isinstance(item, int):
            if item == BRIEF_ALL_I:
                return True
            continue
        raise TypeError(f"{item=} expected {str}")
    return False


def is_verbose(**kwargs) -> bool:
    """Get param `verbose` from `kwargs`"""
    verbose = kwargs.get("verbose")
    if verbose is None:
        return True
    return bool(verbose)


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


# =============================== str ================================

def join(items: LAny) -> str:
    """Joins items by "," """
    return SPLITTER.join([str(i) for i in items])


# ============================= wrapper ==============================

def time_spent(func):
    """Wrapper measure function execution time"""

    def wrap(*args, **kwargs):
        """Wrap"""
        started = time.time()
        return_ = func(*args, **kwargs)
        elapsed = time.time() - started
        print("=== {:s}, spent {:.3f}s ===".format(func.__name__, elapsed))
        return return_

    return wrap
