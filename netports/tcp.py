"""TCP/UDP ports"""

from typing import Any

from netports import helpers as h
from netports.ports import inumbers, parse_range
from netports.range import Range
from netports.static import BRIEF_ALL_I
from netports.types_ import LInt

MIN_PORT = 1
MAX_PORT = 65535
ALL_PORTS_L = list(range(MIN_PORT, MAX_PORT + 1))
ALL_PORTS_S = f"{MIN_PORT}-{MAX_PORT}"


# noinspection PyIncorrectDocstring
def itcp(items: Any = "", **kwargs) -> LInt:
    """Integer TCP/UDP Ports. Sorting TCP/UDP ports and removing duplicates
    ::
        :param items: Range of TCP/UDP ports, can be unsorted and with duplicates
        :type items: str, List[int], List[str]

        :param verbose: True - all ports in verbose mode: [1, 2, ..., 65535],
                        False - all ports in brief mode: [-1], to save RAM (default)
        :type verbose: bool

        :param all: True - Returns all TCP/UDP ports: [1, 2, ..., 65535], or [-1] for verbose=False
        :type all: bool

        :return: *List[int]* of unique sorted TCP/UDP ports
        :rtype: List[int]

        :raises ValueError: If TCP/UDP ports are outside valid range 1...65535

        :example:
            itcp("1,3-5") -> [1, 3, 4, 5]
    """
    if h.is_all(**kwargs):
        if h.is_brief(**kwargs):
            return [BRIEF_ALL_I]
        return ALL_PORTS_L.copy()
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            return [BRIEF_ALL_I]

    ports: LInt = inumbers(items)
    check_tcp_ports(ports)

    if h.is_brief(**kwargs):
        if ports == ALL_PORTS_L:
            return [BRIEF_ALL_I]
    return ports


# noinspection PyIncorrectDocstring
def stcp(items: Any = "", **kwargs) -> str:
    """String TCP/UDP ports. Sorting TCP/UDP ports and removing duplicates
    ::
        :param items: Range of TCP/UDP ports, can be unsorted and with duplicates
        :type items: str, List[int], List[str]

        :param verbose: True - all ports in verbose mode: [1, 2, ..., 65535],
                        False - all ports in brief mode: [-1], to save RAM (default)
        :type verbose: bool

        :param all: True - Returns all TCP/UDP ports: "1-65535"
        :type all: bool

        :return: *str* of unique sorted TCP/UDP ports
        :rtype: str

        :raises ValueError: If TCP/UDP ports are outside valid range 1...65535

        :example:
            stcp([1, 3, 4, 5]) -> "1,3-5"
    """
    if h.is_all(**kwargs):
        return ALL_PORTS_S
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = ",".join(h.lstr(h.remove_brief_items(items)))
            range_o: Range = parse_range(items_)
            check_tcp_ports(range_o.numbers())
            return ALL_PORTS_S

    range_o = parse_range(items)
    check_tcp_ports(range_o.numbers())
    return str(range_o)


# ============================= helpers ==============================

def check_tcp_ports(items: LInt) -> bool:
    """Checks TCP/UDP ports
    ::
        :param items: TCP/UDP ports
        :type items: List[int]

        :return: True if all items are in the valid TCP/UDP range 1...65535
        :rtype: bool

        :raises ValueError: If on of item is outside valid range
    """
    if invalid_port := [i for i in items if i < MIN_PORT or i > MAX_PORT]:
        raise ValueError(f"{invalid_port=}, expected in range 1...65535")
    return True
