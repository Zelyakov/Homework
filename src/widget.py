import re
from typing import List
from datetime import datetime


def get_date(iso_str: str) -> str:
    """
    Преобразует строку с датой/временем в формате ISO 8601 в строку "ДД.ММ.ГГГГ".
    В случае некорректной строки возбуждает ValueError.
    """
    if not isinstance(iso_str, str):
        raise ValueError("Ожидается строка в формате ISO 8601")

    tense = iso_str.strip()
    if tense.endswith("Z"):
        # datetime.fromisoformat не поддерживает 'Z' — заменяем на +00:00
        tense = tense[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(tense)
    except Exception as e:
        raise ValueError(f"Неправильный формат даты: {iso_str}") from e

    return dt.strftime("%d.%m.%Y")


print(get_date("2024-03-11T02:26:18.671407+03:00"))


def mask_account_card(secret: str) -> str:
    """
        Маскирует номер карты или счёта в строке secret.
        - Ищем все подряд идущие цифровые блоки (регуляркой).
        - Берём самое длинное цифровое вхождение (если их несколько).
        - Если рядом (в строке) встречается слово "счет" / "счёт" — считаем это счётом:
            оставляем только последние 4 цифры, остальные заменяем '*'.
        - Иначе, если длина блока напоминает банковскую карту (12-19) —
            оставляем первые 6 и последние 4 цифры (если возможно), остальное маскируем '*'.
        - В других случаях цифровой блок оставляем без изменений.
        Возвращает строку с заменённым (замаскированным) цифровым блоком.
        """
    if not isinstance(secret, str):
        raise TypeError("secret must be a string")

    digit_blocks: List[str] = re.findall(r"\d+", secret)
    if not digit_blocks:
        return secret

    number: str = max(digit_blocks, key=len)

    start_index: int = secret.find(number)
    end_index: int = start_index + len(number)

    lower: str = secret.lower()
    is_account: bool = bool(re.search(r"сч[её]т", lower))

    masked_number: str = number

    if is_account:
        keep = 4
        if len(number) > keep:
            masked_number = "*" * 2 + number[-keep:]
        else:
            masked_number = number
    else:
        if 12 <= len(number) <= 19:
            keep_first = 6
            keep_last = 4
            if len(number) <= (keep_first + keep_last):
                keep_first = max(0, len(number) - keep_last)
            middle_len = len(number) - keep_first - keep_last
            if middle_len > 0:
                masked_number = number[:keep_first] + " " + ("*" * middle_len) + " " + number[-keep_last:]
            else:
                masked_number = number
        else:
            masked_number = number

    return secret[:start_index] + masked_number + secret[end_index:]


print(mask_account_card("Счет 73654108430135874305"))
