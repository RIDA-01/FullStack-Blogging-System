import unittest
from blogging.post import Post

class PostTest(unittest.TestCase):
    def test_post_creation(self):
        p = Post(1, "Hello", "World")
        self.assertEqual(p.post_id, 1)
        self.assertEqual(p.title, "Hello")
        self.assertEqual(p.text, "World")
        