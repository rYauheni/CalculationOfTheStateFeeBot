"""
The module contains general converting functions for courts of all branches.
The converting functions convert the values entered by the user into the values used in the Bot.
"""

import re

from decimal import Decimal, ROUND_HALF_UP


def converting_user_amount(amount: str) -> float:
    """
    The function removes spaces, replaces commas with dots, then uses a regular expression
    to check the value (sum of money) entered by the user against the pattern (digit(1+) dot(0+) digit(0+)).
    If the value matches the pattern and can be converted to a float,
    the function returns the converted value, otherwise, it raises an exception (ValueError)
    :param amount: str
    :return: float
    """
    amount = re.sub(',', '.', amount)
    amount = re.sub(' ', '', amount)
    data_type_check = re.search(r'^\d+\.*\d*$', amount)
    if data_type_check:
        if float(amount) >= 0:
            return float(Decimal(str(amount)).quantize(Decimal('1.00'), ROUND_HALF_UP))
        raise ValueError('Amount (value) must be a string that can be converted to a non-negative number.')
    raise ValueError('Amount (value) must be a string that can be converted to a non-negative number.')


def converting_user_fine(fine: str) -> list:
    """
    The function checks the value (fine and base value or only fine) for the presence of the separator "=".
    If there is a separator "=" and the number of separators is equal to one,
    the function returns a list of two strings:
    the first string is the part of the value before the separator, the second - after.
    In all other cases, a list of one element is returned representing the value entered by the user.
    The use of a separator is necessary if on the day the administrative penalty was imposed and
    on the day the state duty was paid, the base value had a different value
    :param fine: str
    :return: list
    """
    return fine.split('=') if fine.count('=') == 1 else [fine]


def converting_user_pages(number: str) -> int:
    """
    The function checks the value (number of pages) entered by the user.
    If the value contains only digits, the function returns the value converted to an int,
    otherwise, an exception is raised
    :param number: str
    :return: int
    """
    if number.isdigit() and int(number) >= 0:
        return int(number)
    else:
        raise ValueError('Number (value) must be a string that can be converted to a non-negative integer.')


def raise_incorrect_value() -> tuple:
    """
    The function returns responses (tuple of two strings) to the user
    if the user entered a value that does not match the pattern
    :return: tuple
    """
    return (
        'Значение указано некорректно.\nФормат ввода значения:\n'
        '1111 (для целочисленных значений)\nили\n1111.11 (для вещественных значений)',
        '\nПовторно введите значение:'
    )
