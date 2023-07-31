import unittest

from decimal import Decimal, ROUND_HALF_UP

from calc_n_convert_func.EconomicCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property,
    calculating_state_duty_for_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_documents
)

base_value = 37.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_for_property_101(self):
        user_id = 101  # coefficient['instance'] = 1.0; coefficient['claim'] = 1.0
        input_data = [0.0, 1110.31, 3700.0, 3738.14, 18463.0, 18500.0, 18537.01, 36998.84, 37000.0, 37001.16, 115625.02,
                      304621.9, 369998.84, 370000.0, 370001.16, 770961.92, 1156250.0, 1183999.99, 1184000.0,
                      1184001.16, 6423611.1]
        expected_result = [925.0, 925.0, 925.0, 925.0, 925.0, 925.0, 926.85, 1849.94, 1850.0, 1850.03, 4208.75,
                           9878.66, 11839.97, 11840.0, 11840.0, 11840.0, 11840.0, 11840.0, 11840.0, 11840.01,
                           64236.11]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_102(self):
        user_id = 102  # coefficient['instance'] = 1.0; coefficient['claim'] = 0.8
        input_data = [0.0, 1110.31, 3700.0, 3738.14, 18463.0, 18500.0, 18537.01, 36998.84, 37000.0, 37001.16, 115625.02,
                      304621.9, 369998.84, 370000.0, 370001.16, 770961.92, 1156250.0, 1183999.99, 1184000.0,
                      1184001.16, 6423611.1]
        expected_result = [740.0, 740.0, 740.0, 740.0, 740.0, 740.0, 741.48, 1479.95, 1480.0, 1480.02, 3367.0,
                           7902.93, 9471.98, 9472.0, 9472.0, 9472.0, 9472.0, 9472.0, 9472.0, 9472.01, 51388.89]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_103(self):
        user_id = 103  # coefficient['instance'] = 0.8; coefficient['claim'] = 1.0
        input_data = [0.0, 1110.31, 3700.0, 3738.14, 18463.0, 18500.0, 18537.01, 36998.84, 37000.0, 37001.16, 115625.02,
                      304621.9, 369998.84, 370000.0, 370001.16, 770961.92, 1156250.0, 1183999.99, 1184000.0,
                      1184001.16, 6423611.1]
        expected_result = [740.0, 740.0, 740.0, 740.0, 740.0, 740.0, 741.48, 1479.95, 1480.0, 1480.02, 3367.0,
                           7902.93, 9471.98, 9472.0, 9472.0, 9472.0, 9472.0, 9472.0, 9472.0, 9472.01, 51388.89]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_104(self):
        user_id = 104  # coefficient['instance'] = 0.8; coefficient['claim'] = 0.8
        input_data = [0.0, 1110.31, 3700.0, 3738.14, 18463.0, 18500.0, 18537.01, 36998.84, 37000.0, 37001.16, 115625.02,
                      304621.9, 369998.84, 370000.0, 370001.16, 770961.92, 1156250.0, 1183999.99, 1184000.0,
                      1184001.16, 6423611.1]
        expected_result = [592.0, 592.0, 592.0, 592.0, 592.0, 592.0, 593.18, 1183.96, 1184.0, 1184.02, 2693.6,
                           6322.34, 7577.58, 7577.6, 7577.6, 7577.6, 7577.6, 7577.6, 7577.6, 7577.61, 41111.11]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        user_id = 101
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property, el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property, el, base_value, user_id)

    def test_calculating_state_duty_for_order(self):
        input_data = [0.0, 3699.91, 3700.0, 3700.01, 6423.6, 11099.97, 11100.0, 11100.01, 1156250.0]
        expected_result = [74.0, 74.0, 185.0, 185.0, 185.0, 185.0, 259.0, 259.0, 259.0]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_order(el, base_value)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_order_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_order, el, base_value)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_order, el, base_value)

    def test_calculating_state_duty_for_administrative_case_37(self):
        input_data = [0.0, 369.99, 370.0, 370.01, 1284.72, 3699.99, 3700.0, 3700.01, 1027777.77]
        expected_result = [18.5, 18.5, 74.0, 74.0, 74.0, 74.0, 111.0, 111.0, 111.0]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_administrative_case(el, 37, base_value)
            actual_result.append(el_res)
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

    def test_calculating_state_duty_for_get_documents(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [7.4, 8.51, 18.5, 29.6, 30.71, 117.29, 118.4, 1240.61, 986673.08]
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
