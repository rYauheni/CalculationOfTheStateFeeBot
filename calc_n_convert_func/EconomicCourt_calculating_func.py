"""
The module contains calculating functions for EconomicCourt branch.
The calculating functions calculate the reduction coefficient for state duty and
the amount of the state duty in the case when the amount of the state duty depends on the size of the value.
"""

from status_log_db.bot_status_log_db import get_column_value


def calculate_coefficient(user_id: int) -> float:
    """
    The function defines and returns the size of the reduction coefficient in cases specified
    in the Tax Code of the Republic of Belarus
    (for appeal, casstion and supervisory instances and for disputes about the quality of the delivered goods)
    :param user_id: int
    :return: float
    """
    coefficient = 1.0
    if get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in {'appeal', 'cassation', 'supervisory'}:
        coefficient *= 0.8
    if get_column_value(user_id, 'claim') and get_column_value(user_id, 'claim') == 'quality_of_goods_claim':
        coefficient *= 0.8
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
        return (base_value * 25) * coefficient
    elif claim_price * 0.05 >= base_value * 25 and claim_price < base_value * 1000:
        return (claim_price * 0.05) * coefficient
    elif base_value * 1000 <= claim_price < base_value * 10000:
        return (base_value * 1000 * 0.05 + (claim_price - (base_value * 1000)) * 0.03) * coefficient
    elif claim_price >= base_value * 10000:
        if claim_price * 0.01 < base_value * 1000 * 0.05 + base_value * 9000 * 0.03:
            return (base_value * 1000 * 0.05 + base_value * 9000 * 0.03) * coefficient
        return claim_price * 0.01 * coefficient
    else:
        raise ValueError('Claim price (value) must be non-negative number.')


def calculating_state_duty_for_order(amount_of_recovery: float, base_value: float) -> float:
    """
    The function calculates and returns the amount of the state duty for order proceeding
    based on the amount of recovery entered by the user, taking into account the coefficient
    :param amount_of_recovery: float
    :param base_value: float
    :return: float
    """
    # del coefficient
    if 0 <= amount_of_recovery < base_value * 100:
        return base_value * 2
    elif base_value * 100 <= amount_of_recovery < base_value * 300:
        return base_value * 5
    elif amount_of_recovery >= base_value * 300:
        return base_value * 7
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
        return base_value * 0.5
    elif b_v * 10 <= fine < b_v * 100:
        return base_value * 2
    elif fine >= b_v * 100:
        return base_value * 3
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
        return base_value * 0.2 + pages * base_value * 0.03
    else:
        raise ValueError('Pages (value) must be non-negative integer.')
