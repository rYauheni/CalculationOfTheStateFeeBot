import unittest

from decimal import Decimal, ROUND_HALF_UP

from EconomicCourt_calculating_func import (
    calculating_state_duty_for_property,
    calculating_state_duty_for_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_documents
)

from tests.user_id_for_test import user_id

base_value = 32.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_for_property(self):
        input_data = [0, 960.27, 3200, 3232.99, 15968, 16000, 16032.01, 31999, 32000, 32001, 100000.02, 263456.78,
                      319999, 320000, 320001, 666777.88, 1000000, 1023999.99, 1024000, 1024001, 5555555.55]
        expected_result = [800, 800, 800, 800, 800, 800, 801.6, 1599.95, 1600, 1600.03, 3640, 8543.7, 10239.97,
                           10240, 10240, 10240, 10240, 10240, 10240, 10240.01, 55555.56]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property, el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property, el, base_value, user_id)

    def test_calculating_state_duty_for_order(self):
        input_data = [0, 3199.92, 3200, 3200.01, 5555.55, 9599.97, 9600, 9600.01, 1000000]
        expected_result = [64, 64, 160, 160, 160, 160, 224, 224, 224]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_order(el, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_order_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_order, el, base_value)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_order, el, base_value)

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

    def test_calculating_state_duty_for_get_documents(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [6.4, 7.36, 16, 25.6, 26.56, 101.44, 102.4, 1072.96, 853338.88]
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
