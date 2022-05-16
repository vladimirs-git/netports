"""Typing"""
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

DAny = Dict[str, Any]
DiAny = Dict[int, Any]
IInt = Iterable[int]
IStr = Iterable[str]
LAny = List[Any]
LInt = List[int]
LStr = List[str]
OInt = Optional[int]
SInt = Set[int]
SStr = Set[str]
StrInt = Union[int, str]

StrIInt = Union[str, int, IInt]
IStrInt = Union[IStr, IInt]
T2SInt = Tuple[SInt, SInt]
T5Str = Tuple[str, str, str, str, str]
