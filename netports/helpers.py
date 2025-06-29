"""Helper functions."""

import time
from typing import Any, Iterable

from netports.static import BRIEF_ALL_I, BRIEF_ALL_S, SPLITTER
from netports.types_ import LStr, StrInt, IStrInt, LInt


# =============================== bool ===============================


def is_all(**kwargs) -> bool:
    """Get param `all` from `kwargs`."""
    return bool(kwargs.get("all"))


def is_brief(**kwargs) -> bool:
    """Get param `verbose` from `kwargs` and reverse the result."""
    return not is_verbose(**kwargs)


def is_brief_in_items(items: Any) -> bool:
    """Check is "-1" or -1 in `items`, used for verbose=False.

    :param items: str, int, List[str], List[int].
    :return: True - if "-1" or -1 present in `items`.
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
    """Get param `verbose` from `kwargs`."""
    verbose = kwargs.get("verbose")
    if verbose is None:
        return False
    return bool(verbose)


def is_strict(**kwargs) -> bool:
    """Get param `strict` from `kwargs`."""
    strict = kwargs.get("strict")
    if strict is None:
        return True
    return bool(strict)


# =============================== int ================================


def to_int(number: StrInt) -> int:
    """Convert str to int.

    :param number: int or digit as str/
    :return: int.

    :raises TypeError: If number is not digit.
    """
    if isinstance(number, int):
        return number
    if isinstance(number, str) and number.isdigit():
        return int(number)
    raise TypeError(f"{number=} {int} expected")


def to_lint(numbers: IStrInt) -> LInt:
    """Convert List[str] to List[int].

    :param numbers: List[str].
    :return: List[int].
    :raises TypeError: If number is not digit.
    """
    if not isinstance(numbers, (list, set, tuple)):
        raise TypeError(f"{numbers=} {list} expected")
    return [to_int(s) for s in numbers]


# =============================== list ===============================


def lstr(items: Any) -> LStr:
    """Convert any types of items to List[str]."""
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


def remove_brief_items(items: Any) -> list:
    """Remove "-1", -1 from items.

    :param items: str, int, List[str], List[int].
    :return: Items without "-1", -1.
    """
    if isinstance(items, (str, int)):
        items = [items]
    return [i for i in items if i not in (BRIEF_ALL_S, BRIEF_ALL_I)]


def split(items: Any) -> LStr:
    """Split items str, List[str] by "," " "."""
    results: LStr = []
    for items_s in lstr(items):
        for item_s in items_s.split():
            results.extend(item_s.split(SPLITTER))
    return results


# ============================= wrapper ==============================


def time_spent(func):
    """Wrapper measure function execution time."""

    def wrap(*args, **kwargs):
        """Wrap."""
        started = time.time()
        return_ = func(*args, **kwargs)
        elapsed = time.time() - started
        print(f"=== {func.__name__}, spent {elapsed:.3f}s ===")
        return return_

    return wrap
