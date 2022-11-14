import unittest

from decimal import Decimal, ROUND_HALF_UP

from calc_n_convert_func.InternationalArbitrationCourt_calculating_func import (
    calculating_arbitration_fee_for_property_for_resident,
    calculating_arbitration_fee_for_property_for_non_resident
)

from tests.user_id_for_test import user_id

base_value = 32.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_arbitration_fee_for_property_for_resident(self):
        input_data = [0, 1, 1111, 31999.99, 32000, 32002, 319990, 320000, 320006, 6399000, 6400000, 555555555.55]
        expected_result = [1600.0, 1600.0, 1600.0, 1600.0, 1600.0, 1600.06, 10239.7, 10240.0, 10240.06, 71030.0, 71040,
                           1993084.44]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_resident(el, base_value, user_id)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_resident_raise_error(self):
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_arbitration_fee_for_property_for_resident,
                              el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_arbitration_fee_for_property_for_resident, el, base_value, user_id)

    def test_calculating_arbitration_fee_for_property_for_non_resident(self):
        input_data = [0, 1, 4999.99, 5000, 5000.01, 5000.1, 9999.99, 10000, 10001, 24999.99, 25000, 25001, 49999, 50000,
                      50001, 74999, 75000, 75001, 99999, 100000, 100001, 149999, 150000, 150001, 199999, 200000, 200001,
                      499999, 500000, 500001, 999999, 1000000, 1000001, 1999998, 2000000, 2000002, 333333333.33]
        expected_result = [700.0, 700.0, 700.0, 700.0, 700.0, 700.01, 975.0, 975.0, 975.06, 1800.0, 1800.0, 1800.05,
                           3049.95, 3050.0, 3050.05, 4174.96, 4175.00, 4175.04, 5174.96, 5175.0, 5075.04, 6824.97,
                           6825.0, 6825.03, 8324.97, 8325.0, 8325.02, 12824.99, 12825.0, 12825.01, 17824.99, 17825.0,
                           17825.01, 22824.99, 22825.0, 22825.01, 1348158.33]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_non_resident(el, user_id)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_non_resident_raise_error(self):
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_arbitration_fee_for_property_for_non_resident, el, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_arbitration_fee_for_property_for_non_resident, el, user_id)
