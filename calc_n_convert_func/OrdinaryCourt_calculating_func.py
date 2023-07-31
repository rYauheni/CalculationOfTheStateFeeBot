from orm.orm_functions import get_column_value


def calculate_coefficient(user_id: int) -> float:
    coefficient = 1.0
    if get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in {'appeal', 'supervisory'}:
        coefficient *= 0.8
    if get_column_value(user_id, 'criminal') and get_column_value(user_id, 'criminal') == 'in_part_of_civil_lawsuit':
        coefficient *= 0.8
    return coefficient


def calculating_state_duty_for_property_and_order(amount: float, base_value: float, user_id: int) -> float:
    coefficient = calculate_coefficient(user_id)
    if 0 <= amount * 0.05 < base_value * 2:
        return (base_value * 2) * coefficient
    elif amount * 0.05 >= base_value * 2:
        return (amount * 0.05) * coefficient
    else:
        raise ValueError('Amount (value) must be non-negative number.')


def calculating_state_duty_for_administrative_case(fine: float, b_v: float, base_value: float) -> float:
    if 0 <= fine < b_v * 10:
        return base_value * 0.5
    elif b_v * 10 <= fine < b_v * 100:
        return base_value * 2
    elif fine >= b_v * 100:
        return base_value * 3
    else:
        raise ValueError('Fine (value) must be non-negative number.')


def calculating_state_duty_for_get_copy_of_court_order(pages: int, base_value: float) -> float:
    if isinstance(pages, int) and pages >= 0:
        return base_value * 1 + pages * base_value * 0.1
    else:
        raise ValueError('Pages (value) must be non-negative integer.')


def calculating_state_duty_for_get_documents(pages: int, base_value: float) -> float:
    if isinstance(pages, int) and pages >= 0:
        return base_value * 0.1 + pages * base_value * 0.003
    else:
        raise ValueError('Pages (value) must be non-negative integer.')
