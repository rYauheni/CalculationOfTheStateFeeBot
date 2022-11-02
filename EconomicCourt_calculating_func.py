

def calculate_coefficient(status_log: dict) -> float:
    coefficient = 1.0
    if 'instance' in status_log and status_log['instance'] in {'appeal', 'cassation', 'supervisory'}:
        coefficient *= 0.8
    if 'claim' in status_log and status_log['claim'] == 'quality_of_goods_claim':
        coefficient *= 0.8
    return coefficient


def calculating_state_duty_for_property(claim_price: float, base_value: float, status_log: dict) -> float:
    coefficient = calculate_coefficient(status_log)
    if 0 <= claim_price * 0.05 < base_value * 25:
        return base_value * 25 * coefficient
    elif claim_price * 0.05 >= base_value * 25 and claim_price < base_value * 1000:
        return claim_price * 0.05 * coefficient
    elif base_value * 1000 <= claim_price < base_value * 10000:
        return base_value * 1000 * 0.05 + (claim_price - (base_value * 1000)) * 0.03 * coefficient
    elif claim_price >= base_value * 10000:
        if claim_price * 0.01 < base_value * 1000 * 0.05 + base_value * 9000 * 0.03:
            return base_value * 1000 * 0.05 + base_value * 9000 * 0.03 * coefficient
        return claim_price * 0.01 * coefficient
    else:
        raise ValueError('Claim price (value) must be non-negative number.')


def calculating_state_duty_for_order(amount_of_recovery: float, base_value: float, status_log: dict) -> float:
    coefficient = calculate_coefficient(status_log)
    if 0 <= amount_of_recovery < base_value * 100:
        return base_value * 2 * coefficient
    elif base_value * 100 <= amount_of_recovery < base_value * 300:
        return base_value * 5 * coefficient
    elif amount_of_recovery >= base_value * 300:
        return base_value * 7 * coefficient
    else:
        raise ValueError('Amount of recovery (value) must be non-negative number.')


def calculating_state_duty_for_administrative_case(fine: float, b_v: float, base_value: float) -> float:
    if 0 <= fine < b_v * 10:
        return base_value * 0.5
    elif b_v * 10 <= fine < b_v * 100:
        return base_value * 2
    elif fine >= b_v * 100:
        return base_value * 3
    else:
        raise ValueError('Fine (value) must be non-negative number.')


def calculating_state_duty_for_get_documents(pages: int, base_value: float) -> float:
    if isinstance(pages, int) and pages >= 0:
        return base_value * 0.2 + pages * base_value * 0.03
    else:
        raise ValueError('Pages (value) must be non-negative integer.')
