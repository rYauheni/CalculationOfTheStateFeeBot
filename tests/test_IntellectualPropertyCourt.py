import unittest

from decimal import Decimal, ROUND_HALF_UP

from calc_n_convert_func.IntellectualPropertyCourt_calculating_func import (
    calculating_state_duty_for_property,
    calculating_state_duty_for_get_copy_of_court_order_for_entity,
    calculating_state_duty_for_get_copy_of_court_order_for_individual
)

from tests.user_id_for_test import user_id

base_value = 32.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_property_and_order(self):
        input_data = [0, 99.99, 1279.99, 1280, 1280.01, 1280.09, 1280.10, 2000, 7777.77, 444444.44]
        expected_result = [64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.01, 100.0, 388.89, 22222.22]
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

    def test_calculating_state_duty_for_get_copy_of_court_order_for_entity(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [160.0, 176.0, 320.0, 480.0, 496.0, 1744.0, 1760.0, 17936.0, 14222368.0]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order_for_entity(el, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_entity_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_copy_of_court_order_for_entity, el, base_value)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_individual(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [64.0, 73.6, 160.0, 256.0, 265.6, 1014.4, 1024.0, 10729.6, 8533388.8]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order_for_individual(el, base_value)
            el_dec = float(Decimal(str(el_res)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            actual_result.append(el_dec)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_individual_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_copy_of_court_order_for_individual,
                              el, base_value)
