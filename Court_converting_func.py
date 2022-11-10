import re

from decimal import Decimal, ROUND_HALF_UP


def converting_user_amount(amount: str) -> float:
    amount = re.sub(',', '.', amount)
    amount = re.sub(' ', '', amount)
    data_type_check = re.search(r'^\d+\.*\d*$', amount)
    if data_type_check:
        if float(amount) >= 0:
            return float(float(Decimal(str(amount)).quantize(Decimal('1.00'), ROUND_HALF_UP)))
        raise ValueError('Amount (value) must be a string that can be converted to a non-negative number.')
    raise ValueError('Amount (value) must be a string that can be converted to a non-negative number.')


def converting_user_fine(fine: str) -> list:
    return fine.split('=') if fine.count('=') == 1 else [fine]


def converting_user_pages(number: str) -> int:
    if number.isdigit() and int(number) >= 0:
        return int(number)
    else:
        raise ValueError('Number (value) must be a string that can be converted to a non-negative integer.')


def raise_incorrect_value():
    return (
        'Значение указано некорректно.\nФормат ввода значения:\n'
        '1111 (для целочисленных значений)\nили\n1111.11 (для вещественных значений)',
        '\nПовторно введите значение:'
    )
