import unittest

from calc_n_convert_func.InternationalArbitrationCourt_calculating_func import (
    calculating_arbitration_fee_for_property_for_resident,
    calculating_arbitration_fee_for_property_for_non_resident
)

base_value = 37.0


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_arbitration_fee_for_property_for_resident_401(self):
        user_id = 401  # coefficient['instance'] = 1.0; coefficient['proceeding'] = 1.0
        input_data = [0.0, 1.16, 1284.59, 36999.99, 37000.0, 37002.31, 369988.44, 370000.0, 370006.94, 7398843.75,
                      7400000.0, 642361111.1]
        expected_result = [1850.0, 1850.0, 1850.0, 1850.0, 1850.0, 1850.07, 11839.65, 11840.0, 11840.07, 82128.44,
                           82140.0, 2304503.89]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_resident(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_resident_402(self):
        user_id = 402  # coefficient['instance'] = 0.7; coefficient['proceeding'] = 1.0
        input_data = [0.0, 1.16, 1284.59, 36999.99, 37000.0, 37002.31, 369988.44, 370000.0, 370006.94, 7398843.75,
                      7400000.0, 642361111.1]
        expected_result = [1850.0, 1850.0, 1850.0, 1850.0, 1850.0, 1850.0, 8287.76, 8288.0, 8288.05, 57489.91,
                           57498.0, 1613152.72]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_resident(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_resident_403(self):
        user_id = 403  # coefficient['instance'] = 0.7; coefficient['proceeding'] = 0.9
        input_data = [0.0, 1.16, 1284.59, 36999.99, 37000.0, 37002.31, 369988.44, 370000.0, 370006.94, 7398843.75,
                      7400000.0, 642361111.1]
        expected_result = [1850.0, 1850.0, 1850.0, 1850.0, 1850.0, 1850.0, 7458.98, 7459.2, 7459.25, 51740.92,
                           51748.2, 1451837.45]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_resident(el, base_value, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_resident_raise_error(self):
        user_id = 401
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_arbitration_fee_for_property_for_resident,
                              el, base_value, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_arbitration_fee_for_property_for_resident, el, base_value, user_id)

    def test_calculating_arbitration_fee_for_property_for_non_resident_404(self):
        user_id = 404
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
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_non_resident_405(self):
        user_id = 405
        input_data = [0, 1, 4999.99, 5000, 5000.01, 5000.1, 9999.99, 10000, 10001, 24999.99, 25000, 25001, 49999, 50000,
                      50001, 74999, 75000, 75001, 99999, 100000, 100001, 149999, 150000, 150001, 199999, 200000, 200001,
                      499999, 500000, 500001, 999999, 1000000, 1000001, 1999998, 2000000, 2000002, 333333333.33]
        expected_result = [700.0, 700.0, 700.0, 700.0, 700.0, 700.0, 700.0, 700.0, 700.0, 1260.0, 1260.0, 1260.03,
                           2134.96, 2135.0, 2135.04, 2922.47, 2922.5, 2922.53, 3622.47, 3622.50, 3552.53, 4777.48,
                           4777.5, 4777.52, 5827.48, 5827.5, 5827.51, 8977.49, 8977.5, 8977.51, 12477.49, 12477.5,
                           12477.51, 15977.49, 15977.50, 15977.51, 943710.83]
        actual_result = list()
        for el in input_data:
            el_res = calculating_arbitration_fee_for_property_for_non_resident(el, user_id)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_arbitration_fee_for_property_for_non_resident_raise_error(self):
        user_id = 404
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_arbitration_fee_for_property_for_non_resident, el, user_id)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_arbitration_fee_for_property_for_non_resident, el, user_id)
