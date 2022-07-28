"""unittests package"""

import os
import re
import unittest
import pytest
from datetime import datetime

from setup import PACKAGE, ROOT, README

CHANGELOG = "CHANGELOG.rst"


class Test(unittest.TestCase):
    """unittests package"""

    # =========================== helpers ============================

    @staticmethod
    def _paths_dates():
        """path to .py files with last modified dates"""
        paths = []
        for root_i, _, files_i in os.walk(ROOT):
            for file_ in files_i:
                if file_.endswith(".py"):
                    path = os.path.join(root_i, file_)
                    stat = os.stat(path)
                    date_ = datetime.fromtimestamp(stat.st_mtime).date()
                    paths.append((path, date_))
        return paths

    # ============================ tests =============================

    @pytest.mark.skip(reason="developing")
    def test_valid__init__(self):
        """__init__.py"""
        metadata = [
            "__all__ = .+",
            "__version__ = .+",
            "__date__ = .+",
            "__title__ = .+",
            "__summary__ = .+",
            "__author__ = .+",
            "__email__ = .+",
            "__url__ = .+",
            "__download_url__ = .+",
            "__license__ = .+",
        ]
        regex = r"(import|from)\s"
        path = os.path.join(ROOT, PACKAGE, "__init__.py")
        with open(path) as fh:
            lines = {s.strip() for s in fh.read().split("\n")}

            imports = {s for s in lines if re.match(regex, s)}

        for meta in metadata:
            metadata_ = [s for s in lines if re.match(meta, s)]
            self.assertEqual(len(metadata_), 1, msg=f"absent {meta=} in {path=}")

        path = os.path.join(ROOT, "__init__.py")
        with open(path) as fh:
            lines = {s.strip() for s in fh.read().split("\n")}
            imports2 = {s for s in lines if re.match(regex, s)}
            diff = imports2.difference(imports)
            self.assertEqual(len(diff), 0, msg=f"imports {diff=} in {path=} {path=}")

    def test_valid__version(self):
        """version"""
        path = os.path.join(ROOT, PACKAGE, "__init__.py")
        with open(path) as fh:
            text = fh.read()
            version = (re.findall("^__version__ = \"(.+)\"", text, re.M) or [""])[0]
            regex = r"\d+(\.(\d+((a|b|c|rc)\d+)?|post\d+|dev\d+))+"
            self.assertRegex(version, regex, msg=f"__version__ in {path=}")

        path = os.path.join(ROOT, "setup.py")
        with open(path) as fh:
            text = fh.read()
            version_setup = (re.findall("^VERSION = \"(.+)\"", text, re.M) or [""])[0]
            self.assertEqual(version_setup, version, msg=f"VERSION in {path=}")

        path = os.path.join(ROOT, README)
        with open(path) as fh:
            text = fh.read()
            regexes = [
                PACKAGE + r".+/(.+?)\.tar\.gz",
                PACKAGE + r"@(.+?)$",
            ]
            for regex in regexes:
                versions_readme = re.findall(regex, text, re.M)
                for version_readme in versions_readme:
                    self.assertEqual(version_readme, version, msg=f"version in {path=}")

        path = os.path.join(ROOT, CHANGELOG)
        with open(path) as fh:
            text = fh.read()
            regex = r"(.+)\s\(\d\d\d\d-\d\d-\d\d\)$"
            version_changelog = (re.findall(regex, text, re.M) or [""])[0]
            self.assertEqual(version_changelog, version, msg=f"version in {path=}")

    def test_valid__date(self):
        """__date__"""
        path = os.path.join(ROOT, PACKAGE, "__init__.py")
        with open(path) as fh:
            text = fh.read()
            date = (re.findall("^__date__ = \"(.+)\"", text, re.M) or [""])[0]
            self.assertRegex(date, r"\d\d\d\d-\d\d-\d\d", msg=f"date in {path=}")

            # last modified file
            date_last = max([t[1] for t in self._paths_dates()])
            self.assertEqual(date, str(date_last), msg="last modified file")

            path = os.path.join(ROOT, CHANGELOG)
            with open(path) as fh_:
                text = fh_.read()
                regex = r".+\((\d\d\d\d-\d\d-\d\d)\)$"
                date_changelog = (re.findall(regex, text, re.M) or [""])[0]
                self.assertEqual(date_changelog, date, msg=f"date in {path=}")


if __name__ == "__main__":
    unittest.main()
