from fuzzer import fuzz

@fuzz(int, int, iterations=10_000_000)
def test_func(a: int, b: int) -> float:
    """Function with unintended behavior with test purpose.

    Args:
        a (int): numerator of the fraction
        b (int): denominator of the fraction

    Returns:
        float: a divided by b
    """
    return a / b

if __name__ == "__main__":
    test_func(...)
