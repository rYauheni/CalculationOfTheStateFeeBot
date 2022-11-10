from status_log_db.bot_status_log_db import get_column_value


def calculate_coefficient(user_id: int) -> float:
    coefficient = 1.0
    if get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'supervisory':
        coefficient *= 0.8
    return coefficient


def calculating_state_duty_for_property(amount: float, base_value: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount * 0.05 < base_value * 2:
        return base_value * 2 * coefficient
    elif amount * 0.05 >= base_value * 2:
        return amount * 0.05
    else:
        raise ValueError('Amount (value) must be non-negative number.')


def calculating_state_duty_for_get_copy_of_court_order_for_entity(pages: int, base_value: float) -> float:
    if isinstance(pages, int) and pages >= 0:
        return base_value * 5 + pages * base_value * 0.5
    else:
        raise ValueError('Pages (value) must be non-negative integer.')


def calculating_state_duty_for_get_copy_of_court_order_for_individual(pages: int, base_value: float) -> float:
    if isinstance(pages, int) and pages >= 0:
        return base_value * 2 + pages * base_value * 0.3
    else:
        raise ValueError('Pages (value) must be non-negative integer.')
