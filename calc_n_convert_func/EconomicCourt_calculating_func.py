"""
The module contains calculating functions for EconomicCourt branch.
The calculating functions calculate the reduction coefficient for state duty and
the amount of the state duty in the case when the amount of the state duty depends on the size of the value.
"""

from orm.orm_functions import get_column_value

from calc_n_convert_func.rounding_func import round_dec


def calculate_coefficient(user_id: int) -> dict[str, float]:
    """
    The function defines and returns the size of the reduction coefficient in cases specified
    in the Tax Code of the Republic of Belarus
    (for appeal, casstion and supervisory instances and for disputes about the quality of the delivered goods)
    :param user_id: int
    :return: dict[str, float]
    """
    coefficient = {'instance': 1.0, 'claim': 1.0}
    if get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in {'appeal', 'cassation', 'supervisory'}:
        coefficient['instance'] *= 0.8
        coefficient['instance'] = round_dec(coefficient['instance'])
    # must be second if, not elif
    if get_column_value(user_id, 'claim') and get_column_value(user_id, 'claim') == 'quality_of_goods_claim':
        coefficient['claim'] *= 0.8
        coefficient['claim'] = round_dec(coefficient['claim'])
    return coefficient


def calculating_state_duty_for_property(claim_price: float, base_value: float, user_id: int) -> float:
    """
    The function calculates and returns the amount of the state duty for lawsuit proceeding (property claims)
    based on the claim price entered by the user, taking into account the coefficient
    :param claim_price: float
    :param base_value: float
    :param user_id: int
    :return: float
    """
    coefficient = calculate_coefficient(user_id)
    if 0 <= claim_price * 0.05 < base_value * 25:
        state_duty = round_dec(base_value * 25)
        state_duty_with_coefficient = round_dec(round_dec(state_duty * coefficient['claim']) * coefficient['instance'])
        return float(state_duty_with_coefficient)
    elif claim_price * 0.05 >= base_value * 25 and claim_price < base_value * 1000:
        state_duty = round_dec(claim_price * 0.05)
        state_duty_with_coefficient = round_dec(round_dec(state_duty * coefficient['claim']) * coefficient['instance'])
        return float(state_duty_with_coefficient)
    elif base_value * 1000 <= claim_price < base_value * 10000:
        state_duty = round_dec(base_value * 1000 * 0.05 + (claim_price - (base_value * 1000)) * 0.03)
        state_duty_with_coefficient = round_dec(round_dec(state_duty * coefficient['claim']) * coefficient['instance'])
        return float(state_duty_with_coefficient)
    elif claim_price >= base_value * 10000:
        if claim_price * 0.01 < base_value * 1000 * 0.05 + base_value * 9000 * 0.03:
            state_duty = round_dec(base_value * 1000 * 0.05 + base_value * 9000 * 0.03)
            state_duty_with_coefficient = \
                round_dec(round_dec(state_duty * coefficient['claim']) * coefficient['instance'])
            return float(state_duty_with_coefficient)
        state_duty = round_dec(claim_price * 0.01)
        state_duty_with_coefficient = round_dec(round_dec(state_duty * coefficient['claim']) * coefficient['instance'])
        return float(state_duty_with_coefficient)
    else:
        raise ValueError('Claim price (value) must be non-negative number.')


def calculating_state_duty_for_order(amount_of_recovery: float, base_value: float) -> float:
    """
    The function calculates and returns the amount of the state duty for order proceeding
    based on the amount of recovery entered by the user.
    :param amount_of_recovery: float
    :param base_value: float
    :return: float
    """
    # del coefficient
    if 0 <= amount_of_recovery < base_value * 100:
        return float(round_dec(base_value * 2))
    elif base_value * 100 <= amount_of_recovery < base_value * 300:
        return float(round_dec(base_value * 5))
    elif amount_of_recovery >= base_value * 300:
        return float(round_dec(base_value * 7))
    else:
        raise ValueError('Amount of recovery (value) must be non-negative number.')


def calculating_state_duty_for_administrative_case(fine: float, b_v: float, base_value: float) -> float:
    """
    The function calculates and returns the amount of the state duty for administrative cases
    based on the size of fine [size of base value] entered by the user
    :param fine: float
    :param b_v: float
    :param base_value: float
    :return: float
    """
    if 0 <= fine < b_v * 10:
        return float(round_dec(base_value * 0.5))
    elif b_v * 10 <= fine < b_v * 100:
        return float(round_dec(base_value * 2))
    elif fine >= b_v * 100:
        return float(round_dec(base_value * 3))
    else:
        raise ValueError('Fine (value) must be non-negative number.')


def calculating_state_duty_for_get_documents(pages: int, base_value: float) -> float:
    """
    The function calculates and returns the amount of the state duty for get documents
    based on the number of pages entered by the user
    :param pages: float
    :param base_value: float
    :return: float
    """
    if isinstance(pages, int) and pages >= 0:
        return float(round_dec(base_value * 0.2 + pages * base_value * 0.03))
    else:
        raise ValueError('Pages (value) must be non-negative integer.')
