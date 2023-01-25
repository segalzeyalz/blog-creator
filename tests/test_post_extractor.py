import unittest
import uuid

from post_extractor import PostExtractor


class TestPostExtractor(unittest.TestCase):
    def setUp(self):
        self.post_extractor = PostExtractor()

    def test_return_the_amount_of_likes(self):
        post_extractor_with_one_like = self.post_extractor.extract({
            'likes': {
                'avi': True,
                'danny': False
            }
        })
        self.assertEqual(post_extractor_with_one_like["likesAmount"], 1)


if __name__ == '__main__':
    unittest.main()
