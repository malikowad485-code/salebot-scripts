import re
import json
from datetime import datetime


def validate_date(raw):
    """Проверяет дату в форматах ДД.ММ.ГГГГ, ДД/ММ/ГГГГ, ДД-ММ-ГГГГ, ДД ММ ГГГГ (год 2 или 4 цифры)."""
    if not raw:
        return {"date_valid": False, "date_reason": "пустая строка"}

    match = re.match(
        r'^(\d{1,2})[\.\/\-\s](\d{1,2})[\.\/\-\s](\d{2,4})$',
        str(raw).strip()
    )
    if not match:
        return {"date_valid": False, "date_reason": "неверный формат"}

    day, month, year = match.groups()
    day, month, year = int(day), int(month), int(year)

    if year < 100:
        year = 2000 + year if year <= 29 else 1900 + year

    current_year = datetime.now().year
    if year < 1920 or year > current_year:
        return {"date_valid": False, "date_reason": f"год вне диапазона 1920-{current_year}"}

    try:
        dt = datetime(year, month, day)
    except ValueError:
        return {"date_valid": False, "date_reason": "такой даты не существует"}

    return {
        "date_valid": True,
        "date_formatted": dt.strftime("%d.%m.%Y"),
        "day": day,
        "month": month,
        "year": year
    }


def reduce_value(value):
    """Приводит значение к диапазону 1-22, вычитая 22 пока значение больше 22."""
    while value > 22:
        value -= 22
    return value


def sum_digits(number):
    """Складывает все цифры числа (например, 1983 -> 1+9+8+3=21)."""
    return sum(int(digit) for digit in str(number))


def calculate_matrix(day, month, year):
    """Считает все ключевые точки матрицы по формулам."""
    a = reduce_value(day)
    b = reduce_value(month)
    c = reduce_value(sum_digits(year))

    d = reduce_value(a + c)
    x = reduce_value(a + b)
    y = reduce_value(d + x)
    z = reduce_value(d + a)
    f = reduce_value(x + a)
    k = reduce_value(c + b)
    e = reduce_value(k + d)
    n = reduce_value(k + c)
    m = reduce_value(c + d)
    v = reduce_value(k + x)
    l = reduce_value(k + b)
    h = reduce_value(b + x)

    r1 = reduce_value(z + y + f)
    r2 = reduce_value(m + e + n)
    r3 = reduce_value(h + l + v)
    r4 = reduce_value(r1 + r2 + r3)

    return {
        "a": a, "b": b, "c": c, "d": d, "e": e,
        "m": m, "n": n, "v": v, "h": h, "l": l,
        "k": k, "z": z, "y": y, "x": x, "f": f,
        "R1": r1, "R2": r2, "R3": r3, "R4": r4
    }


def handle(data):
    """
    Точка входа для Salebot code_executor.
    Ожидает: {"date": "{$datarojd}"}
    Возвращает JSON с флагом валидности даты и (если дата верна) всеми ключами матрицы.
    """
    raw_date = data.get("date", "")
    result = validate_date(raw_date)

    if result.get("date_valid"):
        matrix = calculate_matrix(result["day"], result["month"], result["year"])
        result.update(matrix)

    return json.dumps(result, ensure_ascii=False)


# --- локальная проверка (не выполняется на сервере Salebot, просто для самопроверки) ---
if __name__ == "__main__":
    test = handle({"date": "29.12.1983"})
    print(test)
