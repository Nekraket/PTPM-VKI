import unittest
from unittest.mock import patch
from src.user_interface import ConsoleUserInterface

class TestConsoleUserInterface(unittest.TestCase):
    def setUp(self):
        self.ui = ConsoleUserInterface()

    @patch('builtins.input', return_value="50")
    def test_get_input_returns_user_value(self, mock_input):
        result = self.ui.get_input("Сторона A: ")
        self.assertEqual(result, "50")
        mock_input.assert_called_once_with("Сторона A: ")

    @patch('builtins.print')
    def test_show_message_prints(self, mock_print):
        self.ui.show_message("Hello")
        mock_print.assert_called_once_with("Hello")