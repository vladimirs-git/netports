"""Examples TCP/UDP"""

import netports

# itcp(items, all)
ports = netports.itcp("80,20,21-22")
print(ports)
# [20, 21, 22, 80]

ports = netports.itcp(["20-22", "80", 22])
print(ports)
# [20, 21, 22, 80]

ports = netports.itcp(all=True)
print(ports)
# [1, 2, ..., 65535]

try:
    netports.itcp("65536")
except ValueError as ex:
    print(ex)
# invalid_port=[65536], expected in range 1...65535


# stcp(items, all)
ports = netports.stcp("80,20-21,80")
print(ports)
# 20-21,80

ports = netports.stcp(["80", "20-21", "20"])
print(ports)
# 20-21,80

ports = netports.stcp([80, 80, 20, 21])
print(ports)
# 20-21,80

ports = netports.stcp(all=True)
print(ports)
# 1-65535

try:
    netports.stcp("65536")
except ValueError as ex:
    print(ex)
# invalid_port=[65536], expected in range 1...65535
