from orm.orm_functions import get_column_value

from calc_n_convert_func.rounding_func import round_dec


def calculate_coefficient(user_id: int) -> dict[str, float]:
    coefficient = {'instance': 1.0, 'proceeding': 1.0}
    if get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'one':
        coefficient['instance'] = 0.7
    if get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'simplified':
        coefficient['instance'] = 0.7
        coefficient['proceeding'] = 0.9
    return coefficient


def calculating_arbitration_fee_for_property_for_resident(amount: float, base_value: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount < base_value * 1000:
        return round_dec(base_value * 50)
    elif base_value * 1000 <= amount < base_value * 10000:
        base_calc = round_dec((base_value * 1000 * 0.05 + (amount - base_value * 1000) * 0.03))
        if round_dec(round_dec(base_calc * coefficient['instance']) * coefficient['proceeding']) < base_value * 50:
            return round_dec(base_value * 50)
        return round_dec(round_dec(base_calc * coefficient['instance']) * coefficient['proceeding'])
    elif base_value * 10000 <= amount <= base_value * 200000:
        base_calc = round_dec(base_value * 1000 * 0.05 + base_value * 9000 * 0.03 +
                              (amount - base_value * 10000) * 0.01)
        return round_dec(round_dec(base_calc * coefficient['instance']) * coefficient['proceeding'])
    elif base_value * 200000 < amount:
        base_calc = round_dec(base_value * 1000 * 0.05 + base_value * 9000 * 0.03 + base_value * 190000 * 0.01 +
                              (amount - base_value * 200000) * 0.0035)
        return round_dec(round_dec(base_calc * coefficient['instance']) * coefficient['proceeding'])
    else:
        raise ValueError('Amount (value) must be non-negative number.')


def calculating_arbitration_fee_for_property_for_non_resident(amount: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount <= 5000:
        return 700.0
    elif 5000 < amount <= 10000:
        base_calc = round_dec(700 + (amount - 5000) * 0.055)
        if round_dec(base_calc * coefficient['instance']) < 700:
            return 700.0
        return round_dec(base_calc * coefficient['instance'])
    elif 10000 < amount <= 25000:
        base_calc = round_dec(975 + (amount - 10000) * 0.055)
        if round_dec(base_calc * coefficient['instance']) < 700:
            return 700.0
        return round_dec(base_calc * coefficient['instance'])
    elif 25000 < amount <= 50000:
        base_calc = round_dec(1800 + (amount - 25000) * 0.05)
        return round_dec(base_calc * coefficient['instance'])
    elif 50000 < amount <= 75000:
        base_calc = round_dec(3050 + (amount - 50000) * 0.045)
        return round_dec(base_calc * coefficient['instance'])
    elif 75000 < amount <= 100000:
        base_calc = round_dec(4175 + (amount - 75000) * 0.04)
        return round_dec(base_calc * coefficient['instance'])
    elif 100000 < amount <= 150000:
        base_calc = round_dec(5075 + (amount - 100000) * 0.035)
        return round_dec(base_calc * coefficient['instance'])
    elif 150000 < amount <= 200000:
        base_calc = round_dec(6825 + (amount - 150000) * 0.03)
        return round_dec(base_calc * coefficient['instance'])
    elif 200000 < amount <= 500000:
        base_calc = round_dec(8325 + (amount - 200000) * 0.015)
        return round_dec(base_calc * coefficient['instance'])
    elif 500000 < amount <= 1000000:
        base_calc = round_dec(12825 + (amount - 500000) * 0.01)
        return round_dec(base_calc * coefficient['instance'])
    elif 1000000 < amount <= 2000000:
        base_calc = round_dec(17825 + (amount - 1000000) * 0.005)
        return round_dec(base_calc * coefficient['instance'])
    elif amount > 2000000:
        base_calc = round_dec(22825 + (amount - 2000000) * 0.004)
        return round_dec(base_calc * coefficient['instance'])
    else:
        raise ValueError('Amount (value) must be non-negative number.')
