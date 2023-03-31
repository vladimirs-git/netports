"""Examples VLAN"""

import re

import netports
from netports import NetportsValueError

# ivlan(items, all, splitter, range_splitter, platform)
config = """
interface FastEthernet0/1
  switchport mode trunk
  switchport trunk allowed vlan 1,3-5
  end
"""
trunk = re.findall("vlan(.+)", config)[0]  # " 1,3-5"
vlans = netports.ivlan(trunk)
print(vlans)
# [1, 3, 4, 5]

vlans = netports.ivlan(["1", "3-4", "4-5"])
print(vlans)
# [1, 3, 4, 5]

ports = netports.ivlan(all=True)
print(ports)
# [1, 2, ..., 4094]

vlans = netports.ivlan("1 3 to 5", platform="hpe")
print(vlans)
# [1, 3, 4, 5]

vlans = netports.ivlan("1 3 to 5", splitter=" ", range_splitter=" to ")
print(vlans)
# [1, 3, 4, 5]

try:
    netports.ivlan("4095")
except NetportsValueError as ex:
    print(ex)
# invalid_vlan=[4095], expected in range 1...4094


# svlan(items, all, splitter, range_splitter, platform)

vlans = netports.svlan("3-4,1,4-5")
print(vlans)
# 1,3-5

vlans = netports.svlan(["1", "3-5", "3-4", "4-5"])
print(vlans)
# 1,3-5

vlans = netports.svlan([1, 3, 4, 5])
print(vlans)
# 1,3-5

ports = netports.svlan(all=True)
print(ports)
# 1-4094

vlans = netports.svlan("1 3 to 5", platform="hpe")
print(vlans)
# 1 3 to 5

vlans = netports.svlan("1 3 to 5", splitter=" ", range_splitter=" to ")
print(vlans)
# 1 3 to 5

try:
    netports.svlan("4095")
except NetportsValueError as ex:
    print(ex)
# invalid_vlan=[4095], expected in range 1...4094
