"""TCP/UDP ports"""

from typing import Any

from netports.ports import inumbers, parse_range
from netports.range import Range
from netports.types_ import LInt


# noinspection PyIncorrectDocstring
def itcp(items: Any = "", **kwargs) -> LInt:
    """**Integer TCP/UDP Ports** - Sorting TCP/UDP ports and removing duplicates
    :param items: Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates
    :param all: True - Return All TCP/UDP ports: [1, 2, ..., 65535]
    :return: *List[int]* of unique sorted TCP/UDP ports
    :raises ValueError: If TCP/UDP ports are outside valid range 1...65535

    :example:
        items: "1,3-5"
        return: [1, 3, 4, 5]
    """
    if bool(kwargs.get("all")):
        return list(range(1, 65536))
    ports: LInt = inumbers(items)
    _check_tcp_ports(ports)
    return ports


# noinspection PyIncorrectDocstring
def stcp(items: Any = "", **kwargs) -> str:
    """**String TCP/UDP Ports** - Sorting TCP/UDP ports and removing duplicates
    :param items: Range of TCP/UDP ports or *List[int]*, can be unsorted and with duplicates
    :param all: True - Return All TCP/UDP ports: "1-65535"
    :return: *str* of unique sorted TCP/UDP ports
    :raises ValueError: If TCP/UDP ports are outside valid range 1...65535

    :example:
        items: [1, 3, 4, 5]
        return: "1,3-5"
    """
    if bool(kwargs.get("all")):
        return "1-65535"
    range_o: Range = parse_range(items)
    _check_tcp_ports(range_o.numbers)
    return str(range_o)


# ============================= helpers ==============================

def _check_tcp_ports(items: LInt) -> bool:
    """Checks TCP/UDP ports
    :param items: TCP/UDP ports
    :return: True if all items are in the valid TCP/UDP range 1...65535
    :raises ValueError: If on of item is outside valid range
    """
    if invalid_port := [i for i in items if i < 1 or i > 65535]:
        raise ValueError(f"{invalid_port=}, expected in range 1...65535")
    return True
