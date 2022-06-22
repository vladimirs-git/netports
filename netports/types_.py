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
TIntStr = Tuple[int, str]

IStrInt = Union[IStr, IInt]
LTIntStr = List[TIntStr]
StrIInt = Union[str, int, IInt]
T2SInt = Tuple[SInt, SInt]
T5Str = Tuple[str, str, str, str, str]
