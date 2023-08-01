import unittest

from decimal import Decimal, ROUND_HALF_UP

from calc_n_convert_func.OrdinaryCourt_calculating_func import (
    calculating_state_duty_for_property_and_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_copy_of_court_order,
    calculating_state_duty_for_get_documents
)

base_value = 37.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_property_and_order_201(self):
        user_id = 201
        input_data = [0.0, 115.61, 1479.99, 1480.0, 1480.01, 1480.1, 1480.12, 2312.5, 8993.05, 513888.88]
        expected_result = [74.0, 74.0, 74.0, 74.0, 74.0, 74.01, 74.01, 115.63, 449.65, 25694.44]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property_and_order(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_property_and_order_202(self):
        user_id = 202
        input_data = [0.0, 115.61, 1479.99, 1480.0, 1480.01, 1480.1, 1480.12, 2312.5, 8993.05, 513888.88]
        expected_result = [59.2, 59.2, 59.2, 59.2, 59.2, 59.21, 59.21, 92.5, 359.72, 20555.55]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property_and_order(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_property_and_order_203(self):
        user_id = 203
        input_data = [0.0, 115.61, 1479.99, 1480.0, 1480.01, 1480.1, 1480.12, 2312.5, 8993.05, 513888.88]
        expected_result = [59.2, 59.2, 59.2, 59.2, 59.2, 59.21, 59.21, 92.5, 359.72, 20555.55]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property_and_order(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        user_id = 201
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property_and_order, el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property_and_order, el, base_value, user_id)

    def test_calculating_state_duty_for_administrative_case_37(self):
        input_data = [0.0, 369.99, 370.0, 370.01, 1284.72, 3699.99, 3700.0, 3700.01, 1027777.77]
        expected_result = [18.5, 18.5, 74.0, 74.0, 74.0, 74.0, 111.0, 111.0, 111.0]
        actual_result = list()
        for el in input_data:
            el_dec = calculating_state_duty_for_administrative_case(el, 37, base_value)
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_administrative_case_29(self):
        input_data = [0, 289.99, 290, 290.01, 320.01, 2899.99, 2900, 2900.01, 444444.44]
        expected_result = [18.5, 18.5, 74.0, 74.0, 74.0, 74.0, 111.0, 111.0, 111.0]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_administrative_case(el, 29, base_value)
            actual_result.append(el_res)
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
        expected_result = [37.0, 40.7, 74.0, 111.0, 114.7, 403.3, 407.0, 4147.7, 3288922.6]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order(el, base_value)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el, base_value)

    def test_calculating_state_duty_for_get_documents(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [3.7, 3.81, 4.81, 5.92, 6.03, 14.69, 14.8, 127.02, 98670.27]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_documents(el, base_value)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_documents_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el, base_value)
