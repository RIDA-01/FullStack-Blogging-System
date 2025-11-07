import unittest
from blogging.post import Post

class PostTest(unittest.TestCase):
    def test_post_creation(self):
        p = Post(1, "Hello", "World")
        self.assertEqual(p.post_id, 1)
        self.assertEqual(p.title, "Hello")
        self.assertEqual(p.text, "World")

    def test_str_and_repr_feel_informative(self):
        # When I print the post, I want a quick glance at id + title.
        p = Post(5, "Title", "Body")
        self.assertIn("[5]", str(p))
        self.assertIn("Title", str(p))
        r = repr(p)
        self.assertIn("Post(", r)
        self.assertIn("post_id=5", r)

    def test_equality_ignores_timestamps(self):
        # Two posts with same user-visible fields should be equal,
        # even if they were created at different times.
        a = Post(3, "Same", "Same")
        b = Post(3, "Same", "Same")
        self.assertEqual(a, b)

    def test_touch_updates_updated_at(self):
        # When I edit a post later, updated_at should move forward.
        p = Post(10, "T", "X")
        old_updated = p.updated_at
        p.touch()
        self.assertGreater(p.updated_at, old_updated)

if __name__ == "__main__":
    unittest.main()
