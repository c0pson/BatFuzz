import pytest

from fuzzer import fuzz

def test_fuzz_decorator():
    call_counter = {'count': 0}

    @fuzz(int, iterations=5)
    def dummy_func(x):
        assert isinstance(x, int)
        call_counter['count'] += 1
    dummy_func()

    assert call_counter['count'] == 5
