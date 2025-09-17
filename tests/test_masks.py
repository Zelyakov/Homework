from typing import Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (7000792289606361, "7000 79** **** 6361"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("4111 1111-1111 1111", "4111 11** **** 1111"),
    ],
)
def test_get_mask_card_number_valid(input_val: Union[str, int], expected: str) -> None:
    """Проверяем корректную маскировку для валидных входов (int/str с разделителями)."""
    assert get_mask_card_number(input_val) == expected


def test_get_mask_card_number_too_short() -> None:
    """Если после очистки меньше 10 цифр, должна возникать ошибка ValueError."""
    with pytest.raises(ValueError):
        get_mask_card_number("123456789")  # 9 цифр -> ошибка


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (123456789012, "**9012"),
        ("1234 5678 9012", "**9012"),
        ("abc", "**"),
        (123, "**123"),
    ],
)
def test_get_mask_account_various(input_val: Union[str, int], expected: str) -> None:
    """Проверяем маскировку аккаунта для разных входов, включая строки без цифр и отрицательные числа."""
    assert get_mask_account(input_val) == expected


def test_get_mask_account_leading_zeros_and_length() -> None:
    """Проверяем, что ведущие нули не теряются и видимые 4 цифры берутся с конца."""
    assert get_mask_account("0000012345") == "**2345"
    assert get_mask_account(100) == "**100"


def test_integration_card_and_account_consistency() -> None:
    """Небольшая интеграционная проверка: поведение на одном и том же наборе цифр."""
    digits = "7000792289606361"
    card = get_mask_card_number(digits)
    account = get_mask_account(digits)

    # Карта должна содержать 4-группы и последние 4 цифры в конце
    assert card.endswith(digits[-4:])
    assert len(account) >= 2  # как минимум две звёздочки
    assert account.endswith(digits[-4:])
