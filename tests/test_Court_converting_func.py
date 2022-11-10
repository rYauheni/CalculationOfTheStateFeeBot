import unittest

from Court_converting_func import (
    converting_user_amount,
    converting_user_fine,
    converting_user_pages
)


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
        input_data_ve = ['12.3.4', '12,3,4', '12.3,4', '12a3', '12.a3', '1a.3', 'abc', '12-34', '.1', '']
        for el in input_data_ve:
            self.assertRaises(ValueError, converting_user_amount, el)

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
            self.assertRaises(ValueError, converting_user_pages, el)
