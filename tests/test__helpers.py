"""unittest helpers.py"""

import unittest

from netports import helpers as h

APOSTROPHE = "'"
SPEECH = "\""


class Test(unittest.TestCase):
    """unittest helpers.py"""

    # ============================= str ==============================

    def test_valid__join(self):
        """join()"""
        for items, expected in [
            ([], ""),
            (["0", "1"], "0,1"),
            ([0, 1], "0,1"),
            ([[1]], "[1]"),
        ]:
            actual = h.join(items=items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    def test_valid__findall1(self):
        """helpers.findall1()"""
        for pattern, string, expected in [
            ("", "abcde", ""),
            ("typo", "abcde", ""),
            ("(typo)", "abcde", ""),
            ("(b)", "abcde", "b"),
            ("(bc)", "abcde", "bc"),
            ("(b)(c)", "abcde", "b"),
        ]:
            actual = h.findall1(pattern=pattern, string=string)
            self.assertEqual(expected, actual, msg=f"{pattern=}")

    def test_valid__findall2(self):
        """helpers.findall2()"""
        for pattern, string, expected in [
            ("", "abcde", ("", "")),
            ("typo", "abcde", ("", "")),
            ("(b)", "abcde", ("", "")),
            ("(b)(typo)", "abcde", ("", "")),
            ("(typo)(c)", "abcde", ("", "")),
            ("(b)(c)", "abcde", ("b", "c")),
            ("(b)(c)(d)", "abcde", ("b", "c")),
        ]:
            actual = h.findall2(pattern=pattern, string=string)
            self.assertEqual(expected, actual, msg=f"{pattern=}")

    def test_valid__findall3(self):
        """helpers.findall3()"""
        for pattern, string, expected in [
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
            actual = h.findall3(pattern=pattern, string=string)
            self.assertEqual(expected, actual, msg=f"{pattern=}")

    def test_valid__findall4(self):
        """findall4()"""
        for pattern, string, req in [
            ("", "abcdef", ("", "", "", "")),
            ("typo", "abcdef", ("", "", "", "")),
            ("(b)", "abcdef", ("", "", "", "")),
            ("(b)(c)(d)(e)", "abcdef", ("b", "c", "d", "e")),
            ("(b)(c)(d)(e)(f)", "abcdef", ("b", "c", "d", "e")),
        ]:
            result = h.findall4(pattern=pattern, string=string)
            self.assertEqual(result, req, msg=f"{pattern=}")

    def test_valid__repr_params(self):
        """init.repr_params()"""
        for args, kwargs, req in [
            ([], {}, ""),
            (["a"], {}, "\"a\""),
            ([], dict(a="a"), "a=\"a\""),
            (["a", "b"], dict(c="c", d="d"), "\"a\", \"b\", c=\"c\", d=\"d\""),
        ]:
            result = h.repr_params(*args, **kwargs)
            result = result.replace(APOSTROPHE, SPEECH)
            self.assertEqual(result, req, msg=f"{kwargs=}")

    # =============================== bool ===============================

    def test_valid__is_all(self):
        """is_all()"""
        for kwargs, expected in [
            ({}, False),
            (dict(all=True), True),
            (dict(all=1), True),
            (dict(all=False), False),
            (dict(verbose=True), False),
        ]:
            actual = h.is_all(**kwargs)
            self.assertEqual(expected, actual, msg=f"{kwargs=}")

    def test_valid__is_brief_all(self):
        """is_brief_all()"""
        for items, expected in [
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
            actual = h.is_brief_in_items(items=items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    def test_valid__is_verbose(self):
        """is_verbose() is_brief()"""
        for kwargs, expected in [
            ({}, False),
            (dict(verbose=True), True),
            (dict(verbose=1), True),
            (dict(verbose=False), False),
            (dict(brief=True), False),
        ]:
            actual = h.is_verbose(**kwargs)
            self.assertEqual(expected, actual, msg=f"{kwargs=}")
            actual = h.is_brief(**kwargs)
            expected = not expected
            self.assertEqual(expected, actual, msg=f"{kwargs=}")

    # ============================= int ==============================

    def test_valid__to_int(self):
        """to_int()"""
        for number, expected in [
            (0, 0),
            ("0", 0),
        ]:
            actual = h.to_int(number)
            self.assertEqual(expected, actual, msg=f"{number=}")

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
        for numbers, expected in [
            ([0, 1, "2"], [0, 1, 2]),
        ]:
            actual = h.to_lint(numbers)
            self.assertEqual(expected, actual, msg=f"{numbers=}")

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
        for items, expected in [
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
            actual = h.lstr(items=items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    def test_invalid__lstr(self):
        """lstr()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.lstr(items=items)

    def test_valid__no_dupl(self):
        """no_dupl()"""
        for members, req in [
            ([], []),
            (["a"], ["a"]),
            (["a", "b", "a"], ["a", "b"]),  # list
            (("a", "b", "a"), ["a", "b"]),  # tuple
            (("b", "a", "b"), ["b", "a"]),
            ([1, 2, 1], [1, 2]),
            ([["a"], ["b"], ["a"]], [["a"], ["b"]]),
            ([{"a": 1}, {"b": 2}, {"a": 1}], [{"a": 1}, {"b": 2}]),
        ]:
            result = h.no_dupl(members)
            self.assertEqual(result, req, msg=f"{members=}")

    def test_valid__remove_brief_items(self):
        """remove_brief_items()"""
        for items, expected in [
            ("", [""]),
            ([], []),
            ([1], [1]),
            (-1, []),
            ("-1", []),
            ([-1, 1], [1]),
            (["-1", "1"], ["1"]),
        ]:
            actual = h.remove_brief_items(items=items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    def test_valid__split(self):
        """split()"""
        for items, expected in [
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
            actual = h.split(items=items)
            self.assertEqual(expected, actual, msg=f"{items=}")

    def test_invalid__split(self):
        """split()"""
        for items, error in [
            (str, TypeError),
        ]:
            with self.assertRaises(error, msg=f"{error=}"):
                h.split(items=items)


if __name__ == "__main__":
    unittest.main()
