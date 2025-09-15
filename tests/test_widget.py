from typing import Any, cast

import pytest

from src.widget import get_date, mask_account_card


def test_get_date_valid_with_offset() -> None:
    s = "2024-03-11T02:26:18.671407+03:00"
    assert get_date(s) == "11.03.2024"


def test_get_date_zulu() -> None:
    # Z (UTC) должен корректно обрабатываться
    assert get_date("2024-03-11T02:26:18Z") == "11.03.2024"


def test_get_date_invalid_type_raises() -> None:
    # cast[Any, ...] используется, чтобы mypy не жаловался на умышленно неверный тип
    with pytest.raises(ValueError):
        get_date(cast(Any, 123))


def test_get_date_bad_format_raises() -> None:
    with pytest.raises(ValueError):
        get_date("not-a-date")


def test_mask_account_card_account_detection() -> None:
    src = "Счет 73654108430135874305"
    assert mask_account_card(src) == "Счет **4305"


def test_mask_account_card_card_detection() -> None:
    src = "Номер карты 7000792289606361"
    # Для карты длиной 16: первые 6, затем 6 '*', затем последние 4
    assert mask_account_card(src) == "Номер карты 700079 ****** 6361"


def test_mask_account_card_short_number_kept() -> None:
    src = "Ref 123456789"
    # Числовой блок длиной 9 не маскируется как карта и возвращается как есть
    assert mask_account_card(src) == "Ref 123456789"


def test_mask_account_card_choose_longest_block() -> None:
    src = "id 12 3456789012345 end"
    # Самый длинный цифровой блок — 3456789012345 (len=13) — маскируется как карта
    assert mask_account_card(src) == "id 12 345678 *** 2345 end"


def test_mask_account_card_non_string_type_raises() -> None:
    with pytest.raises(TypeError):
        mask_account_card(cast(Any, 12345))
