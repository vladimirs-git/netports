"""Example SwVersion."""

import re

from netports import SwVersion

text = "Cisco IOS Software, C2960X Software (C2960X-UNIVERSALK9-M), Version 15.2(4)E10, ..."
text = re.search(r"Version (\S+),", text)[1]

version1 = SwVersion(text)  # 15.2(4)E10
version2 = SwVersion("15.2(4)E11")

assert version1 < version2
assert version1 <= version2
assert not version1 > version2
assert not version1 >= version2
print(version1)
print(version2)
# 15.2(4)e10
# 15.2(4)e11
