"""Typing"""
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

# one-level
DAny = Dict[str, Any]
DStr = Dict[str, str]
DiAny = Dict[int, Any]
IInt = Iterable[int]
IStr = Iterable[str]
LAny = List[Any]
LInt = List[int]
LStr = List[str]
OInt = Optional[int]
SInt = Set[int]
SStr = Set[str]
StrInt = Union[str, int]
T2Str = Tuple[str, str]
T3Str = Tuple[str, str, str]
T4Str = Tuple[str, str, str, str]
T5Str = Tuple[str, str, str, str, str]
TIntStr = Tuple[int, str]

# two-level
DLStr = Dict[str, LStr]
DSStr = Dict[str, SStr]
IStrInt = Union[IStr, IInt]
LT2Str = List[T2Str]
LTIntStr = List[TIntStr]
StrIInt = Union[str, int, IInt]
T2SInt = Tuple[SInt, SInt]
