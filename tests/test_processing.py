import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def empty_data() -> list[dict]:
    return []


@pytest.fixture
def same_date_data() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T00:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2020-01-01T00:00:00"},
        {"id": 3, "state": "PENDING", "date": "2020-01-01T00:00:00"},
    ]


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 2),
    ("PENDING", 0),
])
def test_filter_by_state(sample_data: list[dict], state: str, expected_count: int) -> None:
    result = filter_by_state(sample_data, state)
    assert len(result) == expected_count
    for item in result:
        assert item["state"] == state


def test_filter_by_state_empty(empty_data: list[dict]) -> None:
    assert filter_by_state(empty_data, "EXECUTED") == []


@pytest.mark.parametrize("reverse, expected_order", [
    (True, [41428829, 615064591, 594226727, 939719570]),
    (False, [939719570, 594226727, 615064591, 41428829]),
])
def test_sort_by_date(sample_data: list[dict], reverse: bool, expected_order: list[int]) -> None:
    sorted_data = sort_by_date(sample_data, reverse)
    assert [item["id"] for item in sorted_data] == expected_order


def test_sort_by_date_same_date(same_date_data: list[dict]) -> None:
    sorted_data = sort_by_date(same_date_data)
    assert [item["id"] for item in sorted_data] == [1, 2, 3]


def test_sort_by_date_invalid() -> None:
    with pytest.raises(TypeError):
        sort_by_date("not a list")
    with pytest.raises(ValueError):
        sort_by_date([{"id": 1, "no_date": "2020-01-01"}])