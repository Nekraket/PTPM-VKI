import unittest
from unittest.mock import MagicMock
from src.calculations import Calculator
from src.database import Database
from src.controller import Controller

class TestControllerIntegration(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.db = Database(":memory:")
        self.ui = MagicMock()
        self.notifier = MagicMock()

        self.controller = Controller(self.calc, self.db, self.ui, self.notifier)

    def tearDown(self):
        self.db.close()

    def test_scenario_computes_and_saves_new_triangle(self):
        self.ui.get_input.side_effect = ["50", "50", "50"]

        result = self.controller.run_scenario()

        self.assertEqual(result, "равносторонний")
        record = self.db.get_record("50", "50", "50")
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "равносторонний")
        self.notifier.send.assert_called_once()

    def test_scenario_uses_cache_when_record_exists(self):
        self.db.add_record("3", "4", "5", "разносторонний")

        self.ui.get_input.side_effect = ["3", "4", "5"]

        self.controller.calculator = MagicMock()

        result = self.controller.run_scenario()

        self.assertEqual(result, "разносторонний")
        self.controller.calculator.process_triangle.assert_not_called()

    def test_scenario_sends_result_to_notifier(self):
        self.ui.get_input.side_effect = ["3", "4", "5"]

        self.controller.run_scenario()

        args, _ = self.notifier.send.call_args
        self.assertIn("разносторонний", args[0])

    def test_scenario_with_invalid_input_saves_error(self):
        self.ui.get_input.side_effect = ["abc", "50", "50"]
        result = self.controller.run_scenario()
        self.assertEqual(result, "")
        record = self.db.get_record("abc", "50", "50")
        self.assertIsNotNone(record)

        self.assertEqual(record[1], "Нечисловые данные")