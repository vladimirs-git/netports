"""unittest helpers"""

import unittest
from typing import Callable


class Helpers(unittest.TestCase):
    """Address"""

    def _test_attrs(self, obj, exp_d, msg: str):
        """Test obj.line and attributes in req_d
        :param obj: Tested object
        :param exp_d: Valid attributes and values
        :param msg: Message
        """
        actual = obj.line
        expected = exp_d["line"]
        self.assertEqual(expected, actual, msg=f"{msg} line")
        actual = str(obj)
        self.assertEqual(expected, actual, msg=f"{msg} str")
        for attr, expected in exp_d.items():
            if attr == "numbers":
                method: Callable = getattr(obj, attr)
                actual = method()
            else:
                actual = getattr(obj, attr)
            if hasattr(actual, "line"):
                actual = str(actual)
            self.assertEqual(expected, actual, msg=f"{msg} {attr=}")
