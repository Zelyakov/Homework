import pytest
from typing import Iterable, List

# Подправьте импорт под ваш реальный модуль
from src.transactions import filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "amount": 100.0, "currency": "USD", "description": "Salary"},
        {"id": 2, "amount": 50.5, "currency": "EUR", "description": "Groceries"},
        {"id": 3, "amount": 20, "currency": "USD", "description": "Taxi"},
        {"id": 4, "amount": 0, "currency": "JPY", "description": ""},
        {"id": 5, "amount": 75, "currency": "EUR"},  # без description
    ]


def as_list(maybe_iter: Iterable):
    try:
        return list(maybe_iter)
    except TypeError:
        # если функция возвращает неитерируемый тип — вернём как есть
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


def test_filter_by_currency_generator_does_not_raise(sample_transactions):
    # если функция возвращает генератор — пройдёмся по нему
    result = filter_by_currency(sample_transactions, "EUR")
    for tx in result:
        assert "currency" in tx


def test_transaction_descriptions_basic(sample_transactions):
    descs = transaction_descriptions(sample_transactions)
    assert isinstance(descs, list)
    assert len(descs) == len(sample_transactions)
    for tx, desc in zip(sample_transactions, descs):
        # Ожидаем, что описание содержит сумму и валюту как минимум
        assert str(tx["amount"]) in desc or str(int(tx["amount"])) in desc
        assert tx["currency"] in desc
        # Если есть description в транзакции — текст должен присутствовать
        if "description" in tx and tx["description"]:
            assert tx["description"] in desc


def test_transaction_descriptions_empty():
    assert transaction_descriptions([]) == []
