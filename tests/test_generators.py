import pytest
from typing import Any, List

from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


@pytest.fixture
def sample_transactions() -> List[dict]:
    return [
        {"id": 1, "amount": 100.0, "currency": "USD", "description": "Salary"},
        {"id": 2, "amount": 50.5, "currency": "EUR", "description": "Groceries"},
        {"id": 3, "amount": 20, "currency": "USD", "description": "Taxi"},
        {"id": 4, "amount": 0, "currency": "JPY", "description": ""},
        {"id": 5, "amount": 75, "currency": "EUR"},  # без description
    ]


def as_list(maybe_iter: Any):
    """Попытаться привести к list, если объект итерируемый; иначе вернуть как есть."""
    try:
        return list(maybe_iter)
    except TypeError:
        return maybe_iter


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2, 5]),
        ("JPY", [4]),
        ("GBP", []),  # нет операций в этой валюте
    ],
)
def test_filter_by_currency_returns_only_requested(currency, expected_ids, sample_transactions):
    result = filter_by_currency(sample_transactions, currency)
    items = as_list(result)
    assert isinstance(items, list)
    assert [tx["id"] for tx in items] == expected_ids


def test_filter_by_currency_empty_input():
    result = filter_by_currency([], "USD")
    items = as_list(result)
    assert items == []


def test_filter_by_currency_generator_iterable(sample_transactions):
    """Если возвращается генератор — он итерируем и выдаёт элементы с полем currency."""
    result = filter_by_currency(sample_transactions, "EUR")
    seen = []
    for tx in result:
        assert "currency" in tx
        seen.append(tx)
    assert all(tx["currency"] == "EUR" for tx in seen)


def test_transaction_descriptions_basic(sample_transactions):
    descs = transaction_descriptions(sample_transactions)
    descs_list = as_list(descs)
    assert isinstance(descs_list, list)
    assert len(descs_list) == len(sample_transactions)

    for tx, desc in zip(sample_transactions, descs_list):
        # Ожидаем, что описание содержит сумму и валюту как минимум
        amount = tx.get("amount")
        assert (str(amount) in desc) or (str(int(amount)) in desc)
        assert tx["currency"] in desc
        # Если есть description в транзакции — текст должен присутствовать
        if tx.get("description"):
            assert tx["description"] in desc


def test_transaction_descriptions_empty():
    res = transaction_descriptions([])
    assert as_list(res) == []


def normalize_card(s: str) -> str:
    # удаляем пробелы/тире для сравнения
    return "".join(ch for ch in s if ch.isdigit())


def test_card_number_generator_basic_range():
    gen = card_number_generator(start=7000792289606361, stop=7000792289606364)
    cards = list(gen)
    # Ожидаем 3 элементов, если stop-exclusive, или 4 если включительно; допускаем оба варианта
    assert len(cards) in (3, 4)
    for card in cards:
        assert isinstance(card, str)
        digits = normalize_card(card)
        # допускаем типичные длины карт (15, 16) и возможные длинные варианты
        assert len(digits) in (15, 16, 19)
        groups = [g for g in card.split(" ") if g]
        assert all(g.isdigit() for g in groups)


def test_card_number_generator_edge_cases():
    # крайние значения: одинаковые start и stop
    gen = card_number_generator(start=1234123412341234, stop=1234123412341234)
    cards = list(gen)
    assert len(cards) in (0, 1)
    if cards:
        assert normalize_card(cards[0]) == "1234123412341234"
