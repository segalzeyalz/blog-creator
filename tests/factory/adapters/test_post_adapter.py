import unittest
from factory.adapters.post_adapter import PostAdapter


class TestPostAdapter(unittest.TestCase):
    def setUp(self):
        self.post_adapter = PostAdapter()
    
    def test_adapt(self):
        entity = {
            "postId": 1234,
            "text": "Hello, world!",
            "title": "My first post",
            "likes": [1, 2, 3]
        }
        result = PostAdapter.adapt(entity)
        expected = {
            "post_id": 1234,
            "text": "Hello, world!",
            "title": "My first post",
            "likes": 3
        }
        self.assertEqual(result, expected)

    def test_adapt_query(self):
        entity = {
            "text": "  This is some text  ",
            "title": "  My post title  ",
            "likes.1234": True,
            "likes.5678": False
        }
        result = PostAdapter.adapt_query(entity)
        expected = {
            "$set": {
                "text": "This is some text",
                "title": "My post title",
                "likes.1234": True
            },
            "$unset": {
                "likes.5678": 1
            }
        }
        self.assertEqual(result, expected)

    def test_adapt_remove_trailing_spaces_and_keep_spaces_between(self):
        entity = {"text": "   test        text   ", "title": "   test          title   "}
        self.post_adapter.adapt(entity)
        self.assertEqual(entity["text"], "test        text")
        self.assertEqual(entity["title"], "test          title")


if __name__ == '__main__':
    unittest.main()
