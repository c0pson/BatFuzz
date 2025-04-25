from fuzzer.example_fuzz import fuzz

@fuzz(int, int, iterations=1_000_000)
def test_func(a: int, b: int) -> float:
    return a / b

if __name__ == "__main__":
    test_func((...))
    print('done')
