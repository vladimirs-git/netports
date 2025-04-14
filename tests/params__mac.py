"""Params mac."""
ZERO = "000000000000"
DIGITS = "012345678901"
ABCDEF = "abcdef123456"
FFFFFF = "ffffffffffff"
DOT = "00.00.00.00.00.00"
COLON = "00:00:00:00.00:00"
CISCO = "0000.0000.0000"
HP = "000000-000000"

ZERO_D = {
    "line": "000000000000",
    "hex": "000000000000",
    "cisco": "0000.0000.0000",
    "colon": "00:00:00:00:00:00",
    "hp": "000000-000000",
    "integer": 0,
}

CISCO_D = ZERO_D.copy()
CISCO_D["line"] = CISCO
COLON_D = ZERO_D.copy()
COLON_D["line"] = COLON
HP_D = ZERO_D.copy()
HP_D["line"] = HP