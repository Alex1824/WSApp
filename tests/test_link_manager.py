import unittest
from managers.link_manager import LinkManager

class TestLinkManager(unittest.TestCase):
    def setUp(self):
        self.link_manager = LinkManager()

    def test_clean_phone_number(self):
        # Test valid phone numbers
        self.assertEqual(self.link_manager.clean_phone_number("+1234567890"), "+1234567890")
        self.assertEqual(self.link_manager.clean_phone_number("123-456-7890"), "1234567890")
        
        # Test invalid phone numbers
        self.assertIsNone(self.link_manager.clean_phone_number("abc"))
        self.assertIsNone(self.link_manager.clean_phone_number("123"))  # Too short
        
    def test_generate_link_valid(self):
        """Test generating links with valid phone numbers"""
        # US number format
        success, error = self.link_manager.generate_link("2025550123", "1")
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(self.link_manager.current_link, "https://wa.me/12025550123")
        
        # UK number format
        success, error = self.link_manager.generate_link("7911123456", "44")
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(self.link_manager.current_link, "https://wa.me/447911123456")
        
        # With custom message
        success, error = self.link_manager.generate_link("2025550123", "1", "Hello World")
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(self.link_manager.current_link, "https://wa.me/12025550123?text=Hello%20World")

    def test_generate_link_invalid(self):
        """Test generating links with invalid phone numbers"""
        # Empty phone number
        success, error = self.link_manager.generate_link("", "1")
        self.assertFalse(success)
        self.assertIsNotNone(error)
        
        # Empty country code
        success, error = self.link_manager.generate_link("2025550123", "")
        self.assertFalse(success)
        self.assertIsNotNone(error)
        
        # Invalid number
        success, error = self.link_manager.generate_link("123", "1")
        self.assertFalse(success)
        self.assertIsNotNone(error)

if __name__ == '__main__':
    unittest.main()