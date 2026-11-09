import os
import unittest
from src.parser import ForumParser
from src.database import DatabaseRepository

FIXTURE_PATH = os.path.join('tests', 'fixtures', 'habr_fixture.html')


class TestForumParser(unittest.TestCase):

    def setUp(self):
        self.parser = ForumParser()



    def test_parse_html_returns_all_comments(self):
        with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
            html = f.read()

        comments = self.parser._parse_html(html)

        self.assertEqual(len(comments), 27)

    def test_parse_html_extracts_correct_first_comment(self):
        with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
            html = f.read()

        comments = self.parser._parse_html(html)
        first = comments[0]

        self.assertEqual(first['id'], 26565617)
        self.assertEqual(first['name'], 'yesworldd')

        self.assertIsInstance(first['message'], str)
        self.assertIn('<pre>', first['message'])
        self.assertIn('<code', first['message'])
        self.assertIn('</code>', first['message'])

    def test_parse_html_returns_empty_list_for_empty_html(self):
        comments = self.parser._parse_html('')
        self.assertEqual(comments, [])



    def test_save_to_db_saves_comments(self):
        with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
            html = f.read()

        comments = self.parser._parse_html(html)

        repo = DatabaseRepository(':memory:')
        saved = self.parser.save_to_db(comments, repo)

        self.assertEqual(saved, 27)

        first = repo.get_by_id(26565617)
        self.assertIsNotNone(first)
        self.assertEqual(first['name'], 'yesworldd')
        self.assertIn('<code', first['message'])

    def test_save_to_db_skips_duplicates(self):
        with open(FIXTURE_PATH, 'r', encoding='utf-8') as f:
            html = f.read()

        comments = self.parser._parse_html(html)
        repo = DatabaseRepository(':memory:')

        self.assertEqual(self.parser.save_to_db(comments, repo), 27)

        saved_again = self.parser.save_to_db(comments, repo)
        self.assertEqual(saved_again, 0)


if __name__ == '__main__':
    unittest.main()