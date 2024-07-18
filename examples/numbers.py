"""Examples Numbers."""

import netports

# Sort numbers and removes duplicates
range_o = netports.parse_range("3\t- 5, 1 , 3-5\t,1\n")
print(f"{range_o!r}")
print(range_o.line)
print(range_o.numbers())
# Range("1,3-5")
# 1,3-5
# [1, 3, 4, 5]
print()

# Range with custom splitter and range_splitter
range_o = netports.parse_range("1 3 to 5 1 3 to 5", splitter=" ", range_splitter=" to ")
print(f"{range_o!r}")
print(range_o.line)
print(range_o.numbers())
# Range("1 3 to 5", splitter=" ", range_splitter=" to ")
# 1 3 to 5
# [1, 3, 4, 5]
print()

# Converts unsorted range to sorted List[int] without duplicates
ports = netports.inumbers("3-5,1,3-5,1")
print(ports)
# [1, 3, 4, 5]

ports = netports.inumbers(["3-5,1", "3-4", "1"])
print(ports)
# [1, 3, 4, 5]

ports = netports.inumbers([3, 4, 5, 1, 3, 4, 5, 1])
print(ports)
# [1, 3, 4, 5]
print()

# Converts unsorted range to List[int] with custom splitters
ports = netports.inumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
print(ports)
# [1, 3, 4, 5]
print()

# Converts unsorted range to sorted str without duplicates
ports = netports.snumbers("3-5,1,3-5,1")
print(ports)
# 1,3-5

ports = netports.snumbers(["3-5,1", "3-4", "1"])
print(ports)
# 1,3-5

ports = netports.snumbers([3, 4, 5, 1, 3, 4, 5, 1])
print(ports)
# 1,3-5
print()

# Converts unsorted range to str with custom splitters
ports = netports.snumbers("3 to 5 1 4 to 5 1", splitter=" ", range_splitter=" to ")
print(ports)
# 1 3 to 5
print()
