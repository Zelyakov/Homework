from typing import List, Dict, Any
from typing import List, Dict, Any
from datetime import datetime

def filter_by_state(records: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей из records, у которых ключ 'state' равен указанному значению.
    Значения, где ключ 'state' отсутствует или равен None, игнорируются.
    """
    return [rec for rec in records if rec.get("state") == state]

big_data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

print (filter_by_state(big_data))


def sort_by_date(records: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует записи по полю 'date' (ISO-формат).
    По умолчанию сортировка — по убыванию (новые первыми).
    Некорректные или отсутствующие даты возвращаются в конце результата в исходном порядке.
    """
    # Копируем вход, чтобы не менять оригинал
    valid = []
    invalid = []

    for rec in records:
        date_val = rec.get("date")
        if not isinstance(date_val, str):
            invalid.append(rec)
            continue
        try:
            dt = datetime.fromisoformat(date_val)
        except Exception:
            invalid.append(rec)
        else:
            valid.append((dt, rec))

    # Сортируем валидные записи по datetime
    valid.sort(key=lambda x: x[0], reverse=descending)

    # Возвращаем отсортированные записи (только словари) + некорректные в конце
    return [rec for _, rec in valid] + invalid

date = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

print (sort_by_date(date))
