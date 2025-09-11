from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_basic() -> None:
    processing: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3},  # нет ключа state
        {"id": 4, "state": None},
        {"id": 5, "state": "EXECUTED"},
    ]

    filtered = filter_by_state(processing)  # по умолчанию state="EXECUTED"

    assert isinstance(filtered, list)
    assert [rec["id"] for rec in filtered] == [1, 5]


def test_filter_by_state_custom_state_and_empty() -> None:
    processing: List[Dict[str, Any]] = [
        {"id": 10, "state": "NEW"},
        {"id": 11, "state": "EXECUTED"},
    ]

    res_new = filter_by_state(processing, state="NEW")
    assert [r["id"] for r in res_new] == [10]

    res_none = filter_by_state([])
    assert res_none == []


def test_sort_by_date_basic_descending() -> None:
    # Подготовим набор с валидными и невалидными датами
    processing: List[Dict[str, Any]] = [
        {"id": "a", "date": "2019-07-03T18:35:29.512364"},
        {"id": "b", "date": "2018-06-30T02:08:58.425572"},
        {"id": "c", "date": None},
        {"id": "d", "date": "not-a-date"},
        {"id": "e", "date": "2020-01-01T00:00:00"},
    ]

    sorted_records = sort_by_date(processing)

    # Ожидаем, что валидные даты отсортированы по убыванию (новые первыми),
    # а записи с некорректными датами идут в конце в исходном порядке (c, d).
    assert [r["id"] for r in sorted_records] == ["e", "a", "b", "c", "d"]


def test_sort_by_date_ascending_preserves_invalid_order() -> None:
    processing: List[Dict[str, Any]] = [
        {"id": 1, "date": "2020-01-02T00:00:00"},
        {"id": 2, "date": "2020-01-01T00:00:00"},
        {"id": 3, "date": "bad"},
        {"id": 4, "date": None},
    ]

    sorted_asc = sort_by_date(processing, descending=False)
    assert [r["id"] for r in sorted_asc] == [2, 1, 3, 4]
