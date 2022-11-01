"""unittest helpers.py"""

import unittest

from netports import helpers as h


class Test(unittest.TestCase):
    """unittest helpers.py"""

    # ============================= str ==============================

    def test_valid__join(self):
        """join()"""
        for items, req in [
            ([], ""),
            (["0", "1"], "0,1"),
            ([0, 1], "0,1"),
            ([[1]], "[1]"),
        ]:
            result = h.join(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__findall1(self):
        """helpers.findall1()"""
        for pattern, string, req in [
            ("", "abcde", ""),
            ("typo", "abcde", ""),
            ("(typo)", "abcde", ""),
            ("(b)", "abcde", "b"),
            ("(bc)", "abcde", "bc"),
            ("(b)(c)", "abcde", "b"),
        ]:
            result = h.findall1(pattern=pattern, string=string)
            self.assertEqual(result, req, msg=f"{pattern=}")

    def test_valid__findall2(self):
        """helpers.findall2()"""
        for pattern, string, req in [
            ("", "abcde", ("", "")),
            ("typo", "abcde", ("", "")),
            ("(b)", "abcde", ("", "")),
            ("(b)(typo)", "abcde", ("", "")),
            ("(typo)(c)", "abcde", ("", "")),
            ("(b)(c)", "abcde", ("b", "c")),
            ("(b)(c)(d)", "abcde", ("b", "c")),
        ]:
            result = h.findall2(pattern=pattern, string=string)
            self.assertEqual(result, req, msg=f"{pattern=}")

    def test_valid__findall3(self):
        """helpers.findall3()"""
        for pattern, string, req in [
            ("", "abcde", ("", "", "")),
            ("typo", "abcde", ("", "", "")),
            ("(b)", "abcde", ("", "", "")),
            ("(b)(c)", "abcde", ("", "", "")),
            ("(typo)(c)(d)", "abcde", ("", "", "")),
            ("(b)(typo)(d)", "abcde", ("", "", "")),
            ("(b)(c)(typo)", "abcde", ("", "", "")),
            ("(b)(c)(d)", "abcde", ("b", "c", "d")),
            ("(b)(c)(d)(e)", "abcde", ("b", "c", "d")),
        ]:
            result = h.findall3(pattern=pattern, string=string)
            self.assertEqual(result, req, msg=f"{pattern=}")

    # =============================== bool ===============================

    def test_valid__is_all(self):
        """is_all()"""
        for kwargs, req in [
            ({}, False),
            (dict(all=True), True),
            (dict(all=1), True),
            (dict(all=False), False),
            (dict(verbose=True), False),
        ]:
            result = h.is_all(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    def test_valid__is_brief_all(self):
        """is_brief_all()"""
        for items, req in [
            (1, False),
            ("1", False),
            ([], False),
            ([1], False),
            (["0-1"], False),
            (-1, True),
            ("-1", True),
            ([-1], True),
            (["-1"], True),
            ([1, -1], True),
            (["1", "-1"], True),
        ]:
            result = h.is_brief_in_items(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__is_verbose(self):
        """is_verbose() is_brief()"""
        for kwargs, req in [
            ({}, False),
            (dict(verbose=True), True),
            (dict(verbose=1), True),
            (dict(verbose=False), False),
            (dict(brief=True), False),
        ]:
            result = h.is_verbose(**kwargs)
            self.assertEqual(result, req, msg=f"{kwargs=}")
            result = h.is_brief(**kwargs)
            req = not req
            self.assertEqual(result, req, msg=f"{kwargs=}")

    # ============================= int ==============================

    def test_valid__to_int(self):
        """to_int()"""
        for number, req in [
            (0, 0),
            ("0", 0),
        ]:
            result = h.to_int(number)
            self.assertEqual(result, req, msg=f"{number=}")

    def test_invalid__to_int(self):
        """to_int()"""
        for number, error in [
            ("a", TypeError),
            ("-1", TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.to_int(number)

    def test_valid__to_lint(self):
        """to_lint()"""
        for numbers, req in [
            ([0, 1, "2"], [0, 1, 2]),
        ]:
            result = h.to_lint(numbers)
            self.assertEqual(result, req, msg=f"{numbers=}")

    def test_invalid__to_lint(self):
        """to_lint()"""
        for numbers, error in [
            (1, TypeError),
            (["a"], TypeError),
            (["-1"], TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.to_lint(numbers)

    # ============================= list =============================

    def test_valid__lstr(self):
        """lstr()"""
        for items, req in [
            ("", [""]),
            ("1,3-5", ["1,3-5"]),
            (0, ["0"]),
            (1, ["1"]),
            (b"1", ["1"]),
            (0.9, ["0"]),
            (0.5, ["0"]),
            (1.9, ["1"]),
            ([], []),
            ([0, 1, 1.5, "1.5", "2-4"], ["0", "1", "1", "1.5", "2-4"]),
            ((0, 1), ["0", "1"]),
            ({0: "", 1: ""}, ["0", "1"]),
            ([[1]], ["[1]"]),
        ]:
            result = h.lstr(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__lstr(self):
        """lstr()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.lstr(items=items)

    def test_valid__remove_brief_items(self):
        """remove_brief_items()"""
        for items, req in [
            ("", [""]),
            ([], []),
            ([1], [1]),
            (-1, []),
            ("-1", []),
            ([-1, 1], [1]),
            (["-1", "1"], ["1"]),
        ]:
            result = h.remove_brief_items(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_valid__split(self):
        """split()"""
        for items, req in [
            ("", []),
            ("1,3-5,a", ["1", "3-5", "a"]),
            (0, ["0"]),
            (1, ["1"]),
            (b"1", ["1"]),
            (0.9, ["0"]),
            (0.5, ["0"]),
            (1.9, ["1"]),
            ([], []),
            ([0, 1.5, "1.5", "2-4", "a", "b,c"], ["0", "1", "1.5", "2-4", "a", "b", "c"]),
            ((0, 1), ["0", "1"]),
            ({0: "", 1: ""}, ["0", "1"]),
            ([[1]], ["[1]"]),
        ]:
            result = h.split(items=items)
            self.assertEqual(result, req, msg=f"{items=}")

    def test_invalid__split(self):
        """split()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.split(items=items)


if __name__ == "__main__":
    unittest.main()
