"""Unittest sw_version.py"""

V0 = {
    "public": "0",
    "base_version": "0",
    "release": (0,),
    "major": 0,
    "minor": 0,
    "micro": 0,
    "nano": 0,
}
V1 = {
    "public": "1",
    "base_version": "1",
    "release": (1,),
    "major": 1,
    "minor": 0,
    "micro": 0,
    "nano": 0,
}
V2 = {
    "public": "1.2",
    "base_version": "1.2",
    "release": (1, 2),
    "major": 1,
    "minor": 2,
    "micro": 0,
    "nano": 0,
}
V3 = {
    "public": "1.2.3",
    "base_version": "1.2.3",
    "release": (1, 2, 3),
    "major": 1,
    "minor": 2,
    "micro": 3,
    "nano": 0,
}
V4 = {
    "public": "11.22.33.44",
    "base_version": "11.22.33.44",
    "release": (11, 22, 33, 44),
    "major": 11,
    "minor": 22,
    "micro": 33,
    "nano": 44,
}
V5 = {
    "public": "11.22.33.44.55",
    "base_version": "11.22.33.44",
    "release": (11, 22, 33, 44),
    "major": 11,
    "minor": 22,
    "micro": 33,
    "nano": 44,
}
CISCO1 = {
    "public": "11.22(33)se",
    "base_version": "11.22.33",
    "release": (11, 22, 33),
    "major": 11,
    "minor": 22,
    "micro": 33,
    "nano": 0,
}
CISCO2 = {
    "public": "11.22(33)se44",
    "base_version": "11.22.33.44",
    "release": (11, 22, 33, 44),
    "major": 11,
    "minor": 22,
    "micro": 33,
    "nano": 44,
}
