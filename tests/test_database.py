import unittest
from src.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_record(self):
        self.db.add_record("3", "4", "5", "разносторонний")
        record = self.db.get_record("3", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "разносторонний")

    def test_get_nonexistent_returns_none(self):
        record = self.db.get_record("1", "2", "3")
        self.assertIsNone(record)

    def test_delete_record(self):
        self.db.add_record("3", "4", "5", "разносторонний")
        deleted = self.db.delete_record("3", "4", "5")
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_record("3", "4", "5"))

    def test_delete_nonexistent_returns_false(self):
        deleted = self.db.delete_record("1", "2", "3")
        self.assertFalse(deleted)