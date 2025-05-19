from BatFuzz import fuzz
import random

@fuzz(generations=100)
def test_func() -> None:
    """Function with unintended behavior with test purpose.

    Args:
        a (int): numerator of the fraction
        b (int): denominator of the fraction

    Returns:
        float: a divided by b
    """
    if random.randrange(1,10) == 3:
        raise ZeroDivisionError

if __name__ == "__main__":
    test_func()
