import unittest
from unittest.mock import patch
from src.notifier import EmailNotifier

class TestEmailNotifier(unittest.TestCase):
    def setUp(self):
        self.notifier = EmailNotifier()

    @patch('builtins.print')
    def test_send_returns_true(self, mock_print):
        result = self.notifier.send("Test message")
        self.assertTrue(result)

    @patch('builtins.print')
    def test_send_prints_message(self, mock_print):
        self.notifier.send("Test message")
        mock_print.assert_called_once_with("[EMAIL] Отправлено: Test message")