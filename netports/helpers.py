"""Helper functions."""
import re
import time
from typing import Any, Iterable

from netports.static import BRIEF_ALL_I, BRIEF_ALL_S, SPLITTER
from netports.types_ import LAny, LStr, StrInt, IStrInt, LInt, T2Str, T3Str, T4Str


# =============================== str ================================


def findall1(pattern: str, string: str, flags=0) -> str:
    """Parse 1st item of re.findall(). If nothing is found, returns an empty string.

    Group with parentheses in pattern is required.

    :return: Interested substring.

    :example:
        pattern: "a(b)cde"
        string: "abcde"
        return: "b"
    """
    result = (re.findall(pattern=pattern, string=string, flags=flags) or [""])[0]
    if isinstance(result, str):
        return result
    if isinstance(result, tuple):
        return result[0]
    return ""


def findall2(pattern: str, string: str, flags=0) -> T2Str:
    """Parse 2 items of re.findall(). If nothing is found, returns 2 empty strings.

    Group with parentheses in pattern is required.

    :return: Two interested substrings.

    :example:
        pattern: "a(b)(c)de"
        string: "abcde"
        return: "b", "c"
    """
    result = (re.findall(pattern=pattern, string=string, flags=flags) or [("", "")])[0]
    if isinstance(result, tuple) and len(result) >= 2:
        return result[0], result[1]
    return "", ""


def findall3(pattern: str, string: str, flags=0) -> T3Str:
    """Parse 3 items of re.findall(). If nothing is found, returns 3 empty strings.

    Group with parentheses in pattern is required.

    :return: Three interested substrings.

    :example:
        pattern: "a(b)(c)(d)e"
        string: "abcde"
        return: "b", "c", "d"
    """
    result = (re.findall(pattern=pattern, string=string, flags=flags) or [("", "", "")])[0]
    if isinstance(result, tuple) and len(result) >= 3:
        return result[0], result[1], result[2]
    return "", "", ""


def findall4(pattern: str, string: str, flags=0) -> T4Str:
    """Parse 4 items of re.findall(). If nothing is found, returns 4 empty strings.

    :param pattern: Regex pattern, where 4 groups with parentheses in pattern are required.
    :param string: String where need to find pattern.
    :param flags: findall flags.
    :return: Three interested substrings.

    :example:
        pattern = "a(b)(c)(d)(e)f"
        string = "abcdef"
        return: "b", "c", "d", "e"
    """
    result = (re.findall(pattern=pattern, string=string, flags=flags) or [("", "", "", "")])[0]
    if isinstance(result, tuple) and len(result) >= 4:
        return result[0], result[1], result[2], result[3]
    return "", "", "", ""


def repr_params(*args, **kwargs) -> str:
    """Make params for __repr__() method."""
    args_ = ", ".join([f"{v!r}" for v in args if v])
    kwargs_ = ", ".join([f"{k}={v!r}" for k, v in kwargs.items() if v])
    params = [s for s in (args_, kwargs_) if s]
    return ", ".join(params)


def join(items: LAny) -> str:
    """Join items by ","."""
    return SPLITTER.join([str(i) for i in items])


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


def no_dupl(items: Iterable) -> list:
    """Remove duplicate items from list."""
    items_ = []
    for item in items:
        if item not in items_:
            items_.append(item)
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
        print("=== {:s}, spent {:.3f}s ===".format(func.__name__, elapsed))
        return return_

    return wrap
