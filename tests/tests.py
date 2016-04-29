import unittest

from numeroscadastrais import cpf
from numeroscadastrais.exceptions import *

cpf_string_1 = '111.111.111-11'
cpf_string_1_2 = '11111111111'
cpf_string_2 = '123.456.789-10'

class TestCpf(unittest.TestCase):
    def test_strip_symbols(self):
        self.assertEqual(cpf.strip_symbols('12345678910'), '12345678910')
        self.assertEqual(cpf.strip_symbols('123.456.789-10'), '12345678910')
        self.assertEqual(cpf.strip_symbols(' 123.456.789 10  '), '12345678910')
        self.assertEqual(cpf.strip_symbols('123/456.789-XX'), '123/456789XX')
    
    def test_format(self):
        with self.assertRaises(InvalidCharacters):
            cpf.require_format('123456789XX')
        
        with self.assertRaises(InvalidLength):
            cpf.require_format('1234567891099')
        
        with self.assertRaises(InvalidLength):
            cpf.require_format('123456789')
            
        cpf.require_format('123456789', True)
        cpf.require_format('12345678910', True)
        
        with self.assertRaises(InvalidLength):
            cpf.require_format('1234567891099', True)
    
    def test_calc_check_digit(self):
        self.assertEqual(cpf.calc_check_digit('100000987'), '44')
        self.assertEqual(cpf.calc_check_digit('280012389'), '38')
        self.assertEqual(cpf.calc_check_digit('111111111'), '11')
    
    def test_has_correct_check_digit(self):
        self.assertTrue(cpf.has_correct_check_digit('11111111111'))
        self.assertFalse(cpf.has_correct_check_digit('11111111122'))
    
    def test_is_specifically_invalid_number(self):
        self.assertTrue(cpf.is_specifically_invalid_number('11111111111'))
        self.assertTrue(cpf.is_specifically_invalid_number('22222222222'))
        self.assertTrue(cpf.is_specifically_invalid_number('33333333333'))
        self.assertTrue(cpf.is_specifically_invalid_number('44444444444'))
        self.assertTrue(cpf.is_specifically_invalid_number('55555555555'))
        self.assertTrue(cpf.is_specifically_invalid_number('66666666666'))
        self.assertTrue(cpf.is_specifically_invalid_number('77777777777'))
        self.assertTrue(cpf.is_specifically_invalid_number('88888888888'))
        self.assertTrue(cpf.is_specifically_invalid_number('99999999999'))
        self.assertTrue(cpf.is_specifically_invalid_number('00000000000'))
        self.assertFalse(cpf.is_specifically_invalid_number('12312312312'))
    
    def test_eq(self):
        cpf_1 = cpf.CPF(cpf_string_1)
        cpf_1_2 = cpf.CPF(cpf_string_1_2)
        cpf_2 = cpf.CPF(cpf_string_2)
        
        self.assertEqual(cpf_1, cpf_1)
        self.assertNotEqual(cpf_2, cpf_1)
        self.assertEqual(cpf_1, cpf_1_2)
        
        self.assertTrue(cpf_1.equals_string(cpf_string_1))
        self.assertTrue(cpf_1.equals_string(cpf_string_1_2))
        self.assertFalse(cpf_1.equals_string('abcd'))
        
        self.assertTrue(cpf.compare_strings(cpf_string_1, cpf_string_1))
        self.assertTrue(cpf.compare_strings(cpf_string_1, cpf_string_1_2))
        self.assertFalse(cpf.compare_strings(cpf_string_2, cpf_string_1_2))
        self.assertFalse(cpf.compare_strings(cpf_string_2, cpf_string_1))
        self.assertFalse(cpf.compare_strings(cpf_string_2, 'abcd'))
        self.assertFalse(cpf.compare_strings(cpf_string_2, '1234567'))
        self.assertFalse(cpf.compare_strings('abcd', '1234567'))
    
    def test_hash(self):
        d = {}
        
        cpf_1 = cpf.CPF(cpf_string_1)
        cpf_1_2 = cpf.CPF(cpf_string_1_2)
        cpf_2 = cpf.CPF(cpf_string_2)
        
        d[cpf_1] = 42
        self.assertEqual(d.get(cpf_1), 42)
        self.assertEqual(d.get(cpf_2), None)
        self.assertEqual(d.get(cpf_1_2), 42)
        
        cpf_set = { cpf_1, cpf_2, cpf_1_2 }
        self.assertEqual(len(cpf_set), 2)

