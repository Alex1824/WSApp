import unittest
from src.managers.ad_manager import AdManager

class TestAdManager(unittest.TestCase):
    def setUp(self):
        self.ad_manager = AdManager(app_id="test_app_id")

    def test_show_ad(self):
        """Test showing an ad"""
        result = self.ad_manager.show_ad()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bool)

    def test_check_ad_frequency(self):
        """Test ad frequency check"""
        frequency = self.ad_manager.get_ad_frequency()
        self.assertIsInstance(frequency, int)
        self.assertGreater(frequency, 0)

    def test_update_ad_frequency(self):
        """Test updating ad frequency"""
        new_frequency = 5
        self.ad_manager.set_ad_frequency(new_frequency)
        current_frequency = self.ad_manager.get_ad_frequency()
        self.assertEqual(current_frequency, new_frequency)

if __name__ == '__main__':
    unittest.main()