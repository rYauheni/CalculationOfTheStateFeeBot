import unittest

from config_EconomicCourt import (
    calculating_state_duty_for_property,
    calculating_state_duty_for_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_documents,
    converting_user_amount,
    converting_user_fine,
    converting_user_pages
)


class TestCalculatingFunctions(unittest.TestCase):

    def test_calculating_state_duty_for_property(self):
        input_data = [0, 960.27, 3200, 3232.99, 15968, 16000, 16032.01, 31999, 32000, 32001, 100000.02, 263456.78,
                      319999, 320000, 320001, 666777.88, 1000000, 1023999.99, 1024000, 1024001, 5555555.55]
        expected_result = [800, 800, 800, 800, 800, 800, 801.6, 1599.95, 1600, 1600.03, 3640, 8543.7, 10239.97,
                           10240, 10240, 10240, 10240, 10240, 10240, 10240.01, 55555.56]
        actual_result = list()
        for el in input_data:
            el_res = round(calculating_state_duty_for_property(el), 2)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_property_raise_error(self):
        input_data_ve = [-0.0001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_property, el)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_property, el)

    def test_calculating_state_duty_for_order(self):
        input_data = [0, 3199.92, 3200, 3200.01, 5555.55, 9599.97, 9600, 9600.01, 1000000]
        expected_result = [64, 64, 160, 160, 160, 160, 224, 224, 224]
        actual_result = list()
        for el in input_data:
            el_res = round(calculating_state_duty_for_order(el), 2)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_order_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_order, el)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_order, el)

    def test_calculating_state_duty_for_administrative_case_32(self):
        input_data = [0, 319.99, 320, 320.01, 1111.11, 3199.99, 3200, 3200.01, 888888.88]
        expected_result = [16, 16, 64, 64, 64, 64, 96, 96, 96]
        actual_result = list()
        for el in input_data:
            el_res = round(calculating_state_duty_for_administrative_case(el, 32), 2)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_administrative_case_29(self):
        input_data = [0, 289.99, 290, 290.01, 320.01, 2899.99, 2900, 2900.01, 444444.44]
        expected_result = [16, 16, 64, 64, 64, 64, 96, 96, 96]
        actual_result = list()
        for el in input_data:
            el_res = round(calculating_state_duty_for_administrative_case(el, 29), 2)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_administrative_case_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000]
        input_data_te = ['', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_administrative_case, el, 32)
        for el in input_data_te:
            self.assertRaises(TypeError, calculating_state_duty_for_administrative_case, el, 32)

    def test_calculating_state_duty_for_get_documents(self):
        input_data = [0, 1, 10, 20, 21, 99, 100, 1111, 888888]
        expected_result = [6.4, 7.36, 16, 25.6, 26.56, 101.44, 102.4, 1072.96, 853338.88]
        actual_result = list()
        for el in input_data:
            el_res = round(calculating_state_duty_for_get_documents(el), 2)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_calculating_state_duty_for_get_documents_raise_error(self):
        input_data_ve = [-0.00001, -1, -10000, 0.5, 1.5, 99.99, 0.00001, 4444444.4444444,
                         '', 'abc', '.', '100', '0', [], (), {}]
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el)


class TestConvertingFunctions(unittest.TestCase):

    def test_converting_user_amount(self):
        input_data = ['0123456789', '123   456', '1.556', '1.554', '1 2 3', '12, 34', '12 . 34', '1.']

        expected_result = [123456789.0, 123456.0, 1.56, 1.55, 123.0, 12.34, 12.34, 1.0]
        actual_result = list()
        for el in input_data:
            el_res = converting_user_amount(el)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_converting_user_amount_raise_error(self):
        input_data_ve = ['12.3.4', '12,3,4', '12.3,4', '12a3', '12.a3', '1a.3', 'abc', '12-34', '1.', '.1', '']
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el)

    def test_converting_user_fine(self):
        input_data = ['123=56', '123.25=37', '123=10,22', '1,2=3.4', '1234', '1=2=3', '1=', '=1',
                      'ab=cd', 'a=3', '2=b', 'a,b=c.d']
        expected_result = [['123', '56'], ['123.25', '37'], ['123', '10,22'], ['1,2', '3.4'], ['1234'], ['1=2=3'],
                           ['1', ''], ['', '1'], ['ab', 'cd'], ['a', '3'], ['2', 'b'], ['a,b', 'c.d']]
        actual_result = list()
        for el in input_data:
            el_res = converting_user_fine(el)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_converting_user_pages(self):
        input_data = ['0', '1', '12', '123', '0123456789']
        expected_result = [0, 1, 12, 123, 123456789]
        actual_result = list()
        for el in input_data:
            el_res = converting_user_pages(el)
            actual_result.append(el_res)
        self.assertEqual(expected_result, actual_result)

    def test_converting_user_pages_raise_error(self):
        input_data_ve = ['-2', '-12', '1.', '.1', '12.34', '12,34', '1a', 'b2', 'abc', '34=56', '']
        for el in input_data_ve:
            self.assertRaises(ValueError, calculating_state_duty_for_get_documents, el)
