import unittest
from datetime import datetime
from src.managers.history_manager import HistoryManager

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.history_manager = HistoryManager()

    def test_add_history_entry(self):
        """Test adding a history entry"""
        phone = "+1234567890"
        message = "Hello"
        result = self.history_manager.add_entry(phone, message)
        self.assertTrue(result)
        history = self.history_manager.get_history()
        self.assertGreater(len(history), 0)
        self.assertEqual(history[-1]['phone'], phone)
        self.assertEqual(history[-1]['message'], message)

    def test_clear_history(self):
        """Test clearing history"""
        self.history_manager.add_entry("+1234567890", "Test")
        self.history_manager.clear_history()
        history = self.history_manager.get_history()
        self.assertEqual(len(history), 0)

    def test_get_history_entry(self):
        """Test retrieving specific history entry"""
        phone = "+1234567890"
        message = "Test message"
        self.history_manager.add_entry(phone, message)
        history = self.history_manager.get_history()
        entry = history[-1]
        self.assertIsInstance(entry['timestamp'], datetime)
        self.assertEqual(entry['phone'], phone)
        self.assertEqual(entry['message'], message)

    def test_invalid_history_entry(self):
        """Test adding invalid history entry"""
        result = self.history_manager.add_entry("", "")
        self.assertFalse(result)
        
if __name__ == '__main__':
    unittest.main()