"""TCP/UDP ports"""

from typing import Any

from netports import helpers as h
from netports.exceptions import NetportsValueError
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

        :raises NetportsValueError: If TCP/UDP ports are outside valid range 1...65535

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
    check_ports(ports=ports, strict=True)

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

        :raises NetportsValueError: If TCP/UDP ports are outside valid range 1...65535

        :example:
            stcp([1, 3, 4, 5]) -> "1,3-5"
    """
    if h.is_all(**kwargs):
        return ALL_PORTS_S
    if h.is_brief(**kwargs):
        if h.is_brief_in_items(items):
            items_ = ",".join(h.lstr(h.remove_brief_items(items)))
            range_o: Range = parse_range(items_)
            check_ports(ports=range_o.numbers(), strict=True)
            return ALL_PORTS_S

    range_o = parse_range(items)
    check_ports(ports=range_o.numbers(), strict=True)
    return str(range_o)


def check_port(port: int, strict: bool = False) -> bool:
    """Check TCP/UDP port in the range 1 to 65535.

    :param int port: The TCP/UDP port that needs to be checked.
    :param bool strict: True - raise NetportsValueError if the port is invalid,
        False - return False if the port is invalid. Default is `False`.

    :return: True - If the port is in the valid range of 1 to 65535, False - otherwise.
    :rtype: bool

    :raises TypeError: If the port is not integer.
    :raises NetportsValueError: If strict=True and the port is outside the valid range.
    """
    if not isinstance(port, int):
        raise TypeError(f"{port=} {int} expected.")
    if MIN_PORT <= port <= MAX_PORT:
        return True
    if strict:
        raise NetportsValueError(f"{port=}, expected in the range {MIN_PORT} to {MAX_PORT}")
    return False


def check_ports(ports: LInt, strict: bool = False) -> bool:
    """Check TCP/UDP ports in the range 1 to 65535.

    :param List[int] ports: The TCP/UDP ports that needs to be checked.

    :param bool strict: True - raise NetportsValueError if any in the ports is invalid,
        False - return False if the port is invalid. Default is `False`.

    :return: True - if all ports is in the valid range of 1 to 65535, False - otherwise.
    :rtype: bool

    :raises TypeError: If any in the ports is not integer.
    :raises NetportsValueError: If strict=True and any in the ports is outside the valid range.
    """
    for port in ports:
        if not check_port(port=port, strict=strict):
            return False
    return True
