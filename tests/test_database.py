import unittest
from src.database import DatabaseRepository, ValidationError, DuplicateError


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        self.repo = DatabaseRepository(':memory:')


    def test_add_success(self):
        result = self.repo.add(1, 'alice', 'hello world')
        self.assertTrue(result)

        saved = self.repo.get_by_id(1)
        self.assertIsNotNone(saved)
        self.assertEqual(saved['name'], 'alice')
        self.assertEqual(saved['message'], 'hello world')

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, 'alice', 'first')

        with self.assertRaises(DuplicateError):
            self.repo.add(1, 'bob', 'second')

    def test_add_name_too_long_raises(self):
        """Имя > 256 символов → ValidationError."""
        long_name = 'a' * 257
        with self.assertRaises(ValidationError):
            self.repo.add(1, long_name, 'hello')

    def test_add_message_too_long_raises(self):
        """Сообщение > 8096 символов → ValidationError."""
        long_message = 'x' * 8097
        with self.assertRaises(ValidationError):
            self.repo.add(1, 'alice', long_message)



    def test_get_by_id_success(self):
        self.repo.add(42, 'charlie', 'some text')

        result = self.repo.get_by_id(42)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], 42)
        self.assertEqual(result['name'], 'charlie')
        self.assertEqual(result['message'], 'some text')

    def test_get_by_id_missing_returns_none(self):
        result = self.repo.get_by_id(999)
        self.assertIsNone(result)



    def test_get_by_name_returns_all_matches(self):
        self.repo.add(1, 'alice', 'first')
        self.repo.add(2, 'bob', 'other')
        self.repo.add(3, 'alice', 'second')

        result = self.repo.get_by_name('alice')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        ids = sorted(item['id'] for item in result)
        self.assertEqual(ids, [1, 3])

    def test_get_by_name_unknown_returns_empty_list(self):
        result = self.repo.get_by_name('nobody')
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)



    def test_update_success(self):
        self.repo.add(1, 'alice', 'old text')

        result = self.repo.update(1, 'new text')
        self.assertTrue(result)

        saved = self.repo.get_by_id(1)
        self.assertEqual(saved['message'], 'new text')

    def test_update_missing_id_returns_false(self):
        result = self.repo.update(999, 'whatever')
        self.assertFalse(result)

    def test_update_message_too_long_raises(self):
        self.repo.add(1, 'alice', 'old')
        long_message = 'x' * 8097

        with self.assertRaises(ValidationError):
            self.repo.update(1, long_message)



    def test_delete_success(self):
        self.repo.add(1, 'alice', 'to be deleted')

        result = self.repo.delete(1)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_id_returns_false(self):
        result = self.repo.delete(999)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()