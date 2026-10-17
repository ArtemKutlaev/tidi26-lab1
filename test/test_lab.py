import pytest

from algorithms.binary_search import binary_search_intersection
from algorithms.exponential_search import exp_search
from algorithms.two_binary_search import has_common_element
from algorithms.two_pointers import two_pointers_search

ALL_FUNC = [
    binary_search_intersection,
    exp_search,
    has_common_element,
    two_pointers_search
]

@pytest.mark.parametrize("func",ALL_FUNC)
def test_basic_cases(func):
    assert func([1,2,3], [3,4,5]) is True
    assert func([2,4,6], [1,3,5]) is False
    assert func([],[]) is False
    assert func([1],[1]) is True
    assert func([1,1,1], [1,1,5]) is True
    assert func([10], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]) is True