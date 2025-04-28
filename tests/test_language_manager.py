import unittest
from src.managers.language_manager import LanguageManager

class TestLanguageManager(unittest.TestCase):
    def setUp(self):
        self.language_manager = LanguageManager()

    def test_available_languages(self):
        """Test that we have our supported languages"""
        languages = self.language_manager.get_available_languages()
        self.assertIn('English', languages)
        self.assertIn('Español', languages)
        self.assertIn('Français', languages)

    def test_language_change(self):
        """Test changing languages"""
        # Test changing to a valid language
        self.assertTrue(self.language_manager.change_language('Español'))
        self.assertEqual(self.language_manager.current_language, 'Español')
        
        # Test changing to an invalid language
        self.assertFalse(self.language_manager.change_language('Invalid'))
        self.assertEqual(self.language_manager.current_language, 'Español')  # Should not change

    def test_translations(self):
        """Test that translations work for all languages"""
        test_keys = ['search_country', 'enter_phone', 'custom_message']
        
        for language in self.language_manager.get_available_languages():
            self.language_manager.change_language(language)
            for key in test_keys:
                translated = self.language_manager.get_text(key)
                self.assertNotEqual(translated, key)  # Translation should exist
                self.assertIsInstance(translated, str)  # Should be a string
                self.assertGreater(len(translated), 0)  # Should not be empty

if __name__ == '__main__':
    unittest.main()