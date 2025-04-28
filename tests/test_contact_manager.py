import unittest
from src.managers.contact_manager import ContactManager

class TestContactManager(unittest.TestCase):
    def setUp(self):
        self.contact_manager = ContactManager()

    def test_add_contact(self):
        """Test adding a contact"""
        result = self.contact_manager.add_contact("John Doe", "+1234567890")
        self.assertTrue(result)
        self.assertIn("John Doe", self.contact_manager.get_contacts())

    def test_add_invalid_contact(self):
        """Test adding an invalid contact"""
        result = self.contact_manager.add_contact("", "+1234567890")
        self.assertFalse(result)
        result = self.contact_manager.add_contact("John Doe", "")
        self.assertFalse(result)

    def test_remove_contact(self):
        """Test removing a contact"""
        self.contact_manager.add_contact("John Doe", "+1234567890")
        result = self.contact_manager.remove_contact("John Doe")
        self.assertTrue(result)
        self.assertNotIn("John Doe", self.contact_manager.get_contacts())

    def test_get_contact_number(self):
        """Test retrieving a contact's number"""
        self.contact_manager.add_contact("John Doe", "+1234567890")
        number = self.contact_manager.get_contact_number("John Doe")
        self.assertEqual(number, "+1234567890")
        
if __name__ == '__main__':
    unittest.main()