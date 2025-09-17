from typing import Iterable, Iterator, Mapping, Any, List


def filter_by_currency(
    transactions: Iterable[Mapping[str, Any]], currency: str
) -> Iterator[Mapping[str, Any]]:
    """
    Возвращает итератор транзакций с заданной валютой.
    Пропускает некорректные элементы (не Mapping).
    """
    for tx in transactions:
        if not isinstance(tx, Mapping):
            continue
        if tx.get("currency") == currency:
            yield tx


def transaction_descriptions(transactions: Iterable[Mapping[str, Any]]) -> List[str]:
    """
    Формирует список описаний: сумма + валюта [+ description если есть].
    """
    out: List[str] = []
    for tx in transactions:
        if not isinstance(tx, Mapping):
            continue

        amount = tx.get("amount")
        currency = tx.get("currency")
        desc = tx.get("description")

        amount_part = "0" if amount is None else str(amount)
        currency_part = "" if currency is None else str(currency)

        parts: List[str] = [p for p in (amount_part, currency_part) if p]
        if isinstance(desc, str) and desc:
            parts.append(desc)

        out.append(" ".join(parts))
    return out


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера карт (строки). Диапазон включающий границы: start..stop.
    Формат: группы по 4 цифры, разделённые пробелом.
    """
    if start <= stop:
        rng = range(start, stop + 1)
    else:
        rng = range(0)  # пустой диапазон

    for n in rng:
        digits_only = "".join(ch for ch in str(n) if ch.isdigit())
        if not digits_only:
            continue
        groups = [digits_only[i : i + 4] for i in range(0, len(digits_only), 4)]
        yield " ".join(groups)


__all__ = ["filter_by_currency", "transaction_descriptions", "card_number_generator"]
