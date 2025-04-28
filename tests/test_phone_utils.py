import unittest
from src.core.phone_utils import PhoneUtils

class TestPhoneUtils(unittest.TestCase):
    def setUp(self):
        self.phone_utils = PhoneUtils()

    def test_validate_phone_number(self):
        """Test phone number validation"""
        self.assertTrue(self.phone_utils.validate_number("+1234567890"))
        self.assertTrue(self.phone_utils.validate_number("1234567890"))
        self.assertFalse(self.phone_utils.validate_number("abc"))
        self.assertFalse(self.phone_utils.validate_number(""))

    def test_format_phone_number(self):
        """Test phone number formatting"""
        self.assertEqual(self.phone_utils.format_number("1234567890"), "+1234567890")
        self.assertEqual(self.phone_utils.format_number("+1234567890"), "+1234567890")
        self.assertEqual(self.phone_utils.format_number(""), "")

    def test_clean_phone_number(self):
        """Test phone number cleaning"""
        self.assertEqual(self.phone_utils.clean_number("(123) 456-7890"), "1234567890")
        self.assertEqual(self.phone_utils.clean_number("+1 (123) 456-7890"), "11234567890")
        self.assertEqual(self.phone_utils.clean_number("abc123def"), "123")

if __name__ == '__main__':
    unittest.main()