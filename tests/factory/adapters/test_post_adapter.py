import unittest
from factory.adapters.post_adapter import PostAdapter


class TestPostAdapter(unittest.TestCase):
    def setUp(self):
        self.post_adapter = PostAdapter()

    def test_adapt_remove_trailing_spaces_and_keep_spaces_between(self):
        entity = {"text": "   test        text   ", "title": "   test          title   "}
        self.post_adapter.adapt(entity)
        self.assertEqual(entity["text"], "test        text")
        self.assertEqual(entity["title"], "test          title")


if __name__ == '__main__':
    unittest.main()
