"""unittest helpers"""

import unittest


class Helpers(unittest.TestCase):
    """Address"""

    def _test_attrs(self, obj, req_d, msg: str):
        """Test obj.line and attributes in req_d
        :param obj: Tested object
        :param req_d: Valid attributes and values
        :param msg: Message
        """
        result = obj.line
        req = req_d["line"]
        self.assertEqual(result, req, msg=f"{msg} line")
        result = str(obj)
        self.assertEqual(result, req, msg=f"{msg} str")
        for attr, req in req_d.items():
            result = getattr(obj, attr)
            if hasattr(result, "line"):
                result = str(result)
            self.assertEqual(result, req, msg=f"{msg} {attr=}")
