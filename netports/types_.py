"""Typing"""
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

# 1 level
DAny = Dict[str, Any]
DStr = Dict[str, str]
DiAny = Dict[int, Any]
IInt = Iterable[int]
IStr = Iterable[str]
LAny = List[Any]
LInt = List[int]
LStr = List[str]
OBool = Optional[bool]
OInt = Optional[int]
SInt = Set[int]
SStr = Set[str]
StrInt = Union[str, int]
T2Str = Tuple[str, str]
T3Str = Tuple[str, str, str]
T4Str = Tuple[str, str, str, str]
T5Str = Tuple[str, str, str, str, str]
T6Str = Tuple[str, str, str, str, str, str]
T7Str = Tuple[str, str, str, str, str, str, str]
TIntStr = Tuple[int, str]
TStrInt = Tuple[str, int]

# 2 level
DLStr = Dict[str, LStr]
DSStr = Dict[str, SStr]
IStrInt = Union[IStr, IInt]
LT2Str = List[T2Str]
LTIntStr = List[TIntStr]
OLStr = Optional[LStr]
StrIInt = Union[str, int, IInt]
T2SInt = Tuple[SInt, SInt]

# 3 level
OLT2Str = Optional[LT2Str]
