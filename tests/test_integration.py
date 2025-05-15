import unittest
from managers.link_manager import LinkManager
from src.managers.language_manager import LanguageManager
from src.managers.history_manager import HistoryManager
import tempfile
import os

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for history storage
        self.temp_dir = tempfile.mkdtemp()
        self.link_manager = LinkManager()
        self.language_manager = LanguageManager()
        self.history_manager = HistoryManager(self.temp_dir)
        
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_link_generation_and_history(self):
        """Test that generated links are properly stored in history"""
        # Generate a valid link
        success, error = self.link_manager.generate_link("2025550123", "1")
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Verify link was generated correctly
        expected_link = "https://wa.me/12025550123"
        self.assertEqual(self.link_manager.current_link, expected_link)
        
        # Add to history
        self.history_manager.ad_link(self.link_manager.current_link)
        
        # Verify link is in history
        self.assertIn(expected_link, self.history_manager.history)
        
    def test_multilanguage_link_generation(self):
        """Test link generation with different language settings"""
        # Test in English
        self.language_manager.change_language('English')
        self.link_manager.set_language('English')
        success, error = self.link_manager.generate_link("", "1")
        self.assertFalse(success)
        self.assertTrue("required" in error.lower())
        
        # Test in Spanish
        self.language_manager.change_language('Español')
        self.link_manager.set_language('Español')
        success, error = self.link_manager.generate_link("", "1")
        self.assertFalse(success)
        self.assertTrue("requerido" in error.lower() or "obligatorio" in error.lower())
        
        # Test successful link generation
        success, error = self.link_manager.generate_link("2025550123", "1", "Hola")
        self.assertTrue(success)
        self.assertEqual(self.link_manager.current_link, "https://wa.me/12025550123?text=Hola")

if __name__ == '__main__':
    unittest.main()