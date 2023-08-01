import unittest

from calc_n_convert_func.IntellectualPropertyCourt_calculating_func import (
    calculating_state_duty_for_property,
    calculating_state_duty_for_get_copy_of_court_order_for_entity,
    calculating_state_duty_for_get_copy_of_court_order_for_individual
)


base_value = 37.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_property_and_order_301(self):
        user_id = 301
        input_data = [0.0, 115.61, 1479.99, 1480.0, 1480.01, 1480.1, 1480.12, 2312.5, 8993.05, 513888.88]
        expected_result = [74.0, 74.0, 74.0, 74.0, 74.0, 74.01, 74.01, 115.63, 449.65, 25694.44]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_property_and_order_302(self):
        user_id = 302
        input_data = [0.0, 115.61, 1479.99, 1480.0, 1480.01, 1480.1, 1480.12, 2312.5, 8993.05, 513888.88]
        expected_result = [59.2, 59.2, 59.2, 59.2, 59.2, 59.21, 59.21, 92.5, 359.72, 20555.55]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_property(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        user_id = 301
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property, el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property, el, base_value, user_id)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_entity(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [185.0, 203.5, 370.0, 555.0, 573.5, 2016.5, 2035.0, 20738.5, 16444613.0]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order_for_entity(el, base_value)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_entity_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_copy_of_court_order_for_entity, el, base_value)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_individual(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [74.0, 85.1, 185.0, 296.0, 307.1, 1172.9, 1184.0, 12406.1, 9866730.8]
        actual_result = list()
        for el in input_data:
            el_res = calculating_state_duty_for_get_copy_of_court_order_for_individual(el, base_value)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_copy_of_court_order_for_individual_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_copy_of_court_order_for_individual,
                              el, base_value)
