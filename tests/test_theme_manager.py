import unittest
from src.ui.theme_manager import ThemeManager

class TestThemeManager(unittest.TestCase):
    def setUp(self):
        self.theme_manager = ThemeManager()

    def test_get_current_theme(self):
        """Test getting current theme"""
        theme = self.theme_manager.get_current_theme()
        self.assertIsNotNone(theme)
        self.assertIsInstance(theme, dict)
        self.assertTrue('primary_color' in theme)

    def test_switch_theme(self):
        """Test switching between light and dark themes"""
        initial_theme = self.theme_manager.get_current_theme()
        self.theme_manager.toggle_theme()
        new_theme = self.theme_manager.get_current_theme()
        self.assertNotEqual(initial_theme, new_theme)

    def test_custom_theme(self):
        """Test setting custom theme colors"""
        custom_colors = {
            'primary_color': '#FF0000',
            'secondary_color': '#00FF00',
            'background_color': '#0000FF'
        }
        self.theme_manager.set_custom_theme(custom_colors)
        current_theme = self.theme_manager.get_current_theme()
        self.assertEqual(current_theme['primary_color'], custom_colors['primary_color'])

if __name__ == '__main__':
    unittest.main()