"""Examples Range"""

from netports import Range, NetportsValueError

# Attributes demonstration
range_o = Range("1,3-5")
assert range_o.line == "1,3-5"
assert str(range_o) == "1,3-5"
assert range_o.numbers() == [1, 3, 4, 5]
assert list(range_o) == [1, 3, 4, 5]
assert Range("1,3-5") == Range([1, 3, 4, 5])

# Raise NetportsValueError if one of item is invalid
try:
    Range("1,3-5,typo")
except NetportsValueError as ex:
    print(ex)
# invalid item="typo" in line="1,3-5,typo"

# Make Range without invalid items (not raise NetportsValueError)
range_o = Range("1,3-5,typo", strict=False)
assert range_o.line == "1,3-5"

# Sort numbers and removes duplicates
ranges1 = Range("3-5,1")
print(ranges1)
# 1,3-5

ranges2 = Range("3-5,1,3-5,1,3-4,4-5")
print(ranges2)
# 1,3-5

assert ranges1 == ranges2

# Range with custom splitters
range_o = Range("1, 3-5, 7-9", splitter=", ")
assert range_o.line == "1, 3-5, 7-9"
assert range_o.numbers() == [1, 3, 4, 5, 7, 8, 9]

range_o = Range("1 3 to 5 7 to 9", splitter=" ", range_splitter=" to ")
assert range_o.line == "1 3 to 5 7 to 9"
assert range_o.numbers() == [1, 3, 4, 5, 7, 8, 9]

# Range operators
range_o = Range("1,3") + Range("3-5")
assert str(range_o) == "1,3-5"

range_o = Range("1-5") - Range("2")
assert str(range_o) == "1,3-5"

assert range_o[1] == 3
assert range_o[1:3] == [3, 4]

for number in Range("1,3-5"):
    print(number)
print()
# 1
# 3
# 4
# 5


# Range methods
range_o = Range("1,3") + Range("3-5")
print(range_o)
# 1,3-5

range_o.append(2)
print(range_o)
# 1-5

print(range_o.difference(Range("2,4")))
# 1,3,5

range_o.difference_update(Range("2,4"))
print(range_o)
# 1,3,5

range_o.discard(3)
print(range_o)
# 1,5

range_o.extend([3, 4])
print(range_o)
# 1,3-5

print(range_o.index(5))
# 3

print(range_o.intersection(Range("1-4")))
# 1,3-4

range_o.intersection_update(Range("1-4"))
print(range_o)
# 1,3-4

print(range_o.pop())
print(range_o)
# 4
# 1,3

range_o.remove(3)
print(range_o)
# 1

range_o.update(Range("3,4,5"))
print(range_o)
# 1,3-5
