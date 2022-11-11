from status_log_db.bot_status_log_db import get_column_value


def calculate_coefficient(user_id: int) -> float:
    coefficient = 1.0
    if get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'one':
        coefficient *= 0.7
    if get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'simplified':
        coefficient *= 0.9
    return coefficient


def calculating_state_duty_for_property_for_resident(amount: float, base_value: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount < base_value * 1000:
        return base_value * 50
    elif base_value * 1000 <= amount < base_value * 10000:
        if (base_value * 1000 * 0.05 + (amount - base_value * 1000) * 0.03) * coefficient < base_value * 50:
            return base_value * 50
        return (base_value * 1000 * 0.05 + (amount - base_value * 1000) * 0.03) * coefficient
    elif base_value * 10000 <= amount <= base_value * 200000:
        return (base_value * 1000 * 0.05 + base_value * 9000 * 0.03 + (amount - base_value * 10000) * 0.01) \
               * coefficient
    elif base_value * 200000 < amount:
        return (base_value * 1000 * 0.05 + base_value * 9000 * 0.03 + base_value * 190000 * 0.01 +
                (amount - base_value * 200000) * 0.0035) * coefficient
    else:
        raise ValueError('Amount (value) must be non-negative number.')


def calculating_state_duty_for_property_for_non_resident(amount: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount <= 5000:
        return 700.0
    elif 5000 < amount <= 10000:
        if (700 + (amount - 5000) * 0.055) * coefficient < 700:
            return 700.0
        return (700 + (amount - 5000) * 0.055) * coefficient
    elif 10000 < amount <= 25000:
        if (975 + (amount - 10000) * 0.055) * coefficient < 700:
            return 700.0
        return (975 + (amount - 10000) * 0.055) * coefficient
    elif 25000 < amount <= 50000:
        return (1800 + (amount - 25000) * 0.05) * coefficient
    elif 50000 < amount <= 75000:
        return (3050 + (amount - 50000) * 0.045) * coefficient
    elif 75000 < amount <= 100000:
        return (4175 + (amount - 75000) * 0.04) * coefficient
    elif 100000 < amount <= 150000:
        return (5075 + (amount - 100000) * 0.035) * coefficient
    elif 150000 < amount <= 200000:
        return (6825 + (amount - 150000) * 0.03) * coefficient
    elif 200000 < amount <= 500000:
        return (8325 + (amount - 200000) * 0.015) * coefficient
    elif 500000 < amount <= 1000000:
        return (12825 + (amount - 500000) * 0.01) * coefficient
    elif 1000000 < amount <= 2000000:
        return (17825 + (amount - 1000000) * 0.005) * coefficient
    elif amount > 2000000:
        return (22825 + (amount - 2000000) * 0.004) * coefficient
    else:
        raise ValueError('Amount (value) must be non-negative number.')
