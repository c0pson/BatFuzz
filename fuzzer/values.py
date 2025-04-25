from enum import IntEnum

from sys import maxsize

class SIZE(IntEnum):
    MAX_INT = maxsize
    MIN_INT = -maxsize - 1
