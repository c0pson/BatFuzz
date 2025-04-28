from enum import IntEnum

from sys import maxsize

class SIZE(IntEnum):
    """Represents system-dependent integer size limits.

    Attributes:
        MAX_INT (int): The maximum integer value supported by the platform.
        MIN_INT (int): The minimum integer value, equal to -sys.maxsize - 1.
    """
    MAX_INT = maxsize
    MIN_INT = -maxsize - 1
