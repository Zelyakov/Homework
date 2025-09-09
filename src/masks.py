from typing import Union, overload


@overload
def get_mask_card_number(card_number: int) -> str:  # pragma: no cover - overloads for typing only
    ...


@overload
def get_mask_card_number(card_number: str) -> str:  # pragma: no cover - overloads for typing only
    ...


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Маскирует номер карты: видны первые 6 и последние 4 цифры.
    Формат вывода: блоки по 4 цифры, разделённые пробелом.

    Пример:
        "7000792289606361" -> "7000 79** **** 6361"

    Вход:
        card_number: str или int, содержащий только цифры (входные пробелы/тире игнорируются).
    Возвращает:
        str — замаскированный номер.
    Исключения:
        ValueError — если после очистки нет достаточного количества цифр (меньше 10).
    """

    # Преобразуем в строку и оставим только цифры
    subsequence = str(card_number)
    digits = "".join(i for i in subsequence if i.isdigit())

    # Проверка минимальной длины: необходимо показать 6+4 = 10 видимых цифр
    if len(digits) < 10:
        raise ValueError(
            "Номер должен содержать минимум 10 цифр для маскировки (6 видимых в начале и 4 в конце)."
        )

    # Видимые части
    left_visible = digits[:6]
    right_visible = digits[-4:]

    # Средняя часть, которую нужно замаскировать — длина зависит от длины входа
    middle_len = len(digits) - 10
    middle_mask = "*" * middle_len

    # Соединяем всё и разбиваем по 4 для финального формата
    combined = left_visible + middle_mask + right_visible
    groups = [combined[i : i + 4] for i in range(0, len(combined), 4)]
    return " ".join(groups)


@overload
def get_mask_account(account: int) -> str:  # pragma: no cover - overloads for typing only
    ...


@overload
def get_mask_account(account: str) -> str:  # pragma: no cover - overloads for typing only
    ...


def get_mask_account(account: Union[str, int]) -> str:
    """
    Принимает на вход номер счёта и возвращает его маску.
    Номер счета замаскирован и отображается в формате **XXXX,
    где X — это цифра номера. То есть видны только последние 4 цифры номера,
    а перед ними — две звездочки.

    Если в входе нет цифр — возвращается "**".
    """

    number_check = str(account)
    check = "".join(i for i in number_check if i.isdigit())

    if not check:
        return "**"

    visible = check[-4:]
    mask_visible = "**" + visible
    return mask_visible


__all__ = ["get_mask_card_number", "get_mask_account"]
