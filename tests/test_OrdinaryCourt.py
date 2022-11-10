import unittest

from decimal import Decimal, ROUND_HALF_UP

from calc_n_convert_func.OrdinaryCourt_calculating_func import (
    calculating_state_duty_for_property_and_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_copy_of_court_order,
    calculating_state_duty_for_get_documents
)

from tests.user_id_for_test import user_id

base_value = 32.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_property_and_order(self):
        input_data = [0, 99.99, 1279.99, 1280, 1280.01, 1280.09, 1280.10, 2000, 7777.77, 444444.44]
        expected_result = [64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.01, 100.0, 388.89, 22222.22]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property_and_order(el, base_value, user_id)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property_and_order, el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property_and_order, el, base_value, user_id)

    def test_calculating_state_duty_for_administrative_case_32(self):
        input_data = [0, 319.99, 320, 320.01, 1111.11, 3199.99, 3200, 3200.01, 888888.88]
        expected_result = [16, 16, 64, 64, 64, 64, 96, 96, 96]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_administrative_case(el, 32, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_administrative_case_29(self):
        input_data = [0, 289.99, 290, 290.01, 320.01, 2899.99, 2900, 2900.01, 444444.44]
        expected_result = [16, 16, 64, 64, 64, 64, 96, 96, 96]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_administrative_case(el, 29, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_administrative_case_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_administrative_case, el, 32, base_value)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_administrative_case, el, 32, base_value)

    def test_calculating_state_duty_for_get_copy_of_court_order(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [32.0, 35.2, 64.0, 96.0, 99.2, 348.8, 352.0, 3587.2, 2844473.6]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order(el, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el, base_value)

    def test_calculating_state_duty_for_get_documents(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [3.2, 3.3, 4.16, 5.12, 5.22, 12.7, 12.8, 109.86, 85336.45]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_documents(el, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_documents_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el, base_value)
