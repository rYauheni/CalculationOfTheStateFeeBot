from decimal import Decimal, ROUND_HALF_UP


def round_dec(input_value: (str, int, float)) -> float:
    round_value = float(Decimal(str(input_value)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    return round_value
