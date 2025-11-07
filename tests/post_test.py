import unittest
import datetime
from blogging.post import Post


class TestPost(unittest.TestCase):
    """
    Unit tests for the Post class functionality.
    Tests post creation, equality, timestamps, and string representations.
    """
    
    def test_post_creation(self):
        """Test that a Post object is created with correct attributes and timestamps."""
        post = Post(1, "Test Title", "Test content here")
        
        # Test basic attributes
        self.assertEqual(post.post_id, 1)
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.text, "Test content here")
        
        # Test timestamps exist and are datetime objects
        self.assertIsInstance(post.created_at, datetime.datetime)
        self.assertIsInstance(post.updated_at, datetime.datetime)
        
        # Initially created_at and updated_at should be the same
        self.assertEqual(post.created_at, post.updated_at)
    
    def test_post_equality_same_data(self):
        """Test that two Post objects with same data are equal."""
        post1 = Post(1, "Same Title", "Same content")
        post2 = Post(1, "Same Title", "Same content")
        self.assertEqual(post1, post2)
    
    def test_post_inequality_different_id(self):
        """Test that posts with different IDs are not equal."""
        post1 = Post(1, "Same Title", "Same content")
        post2 = Post(2, "Same Title", "Same content")
        self.assertNotEqual(post1, post2)
    
    def test_post_inequality_different_title(self):
        """Test that posts with different titles are not equal."""
        post1 = Post(1, "Title One", "Same content")
        post2 = Post(1, "Title Two", "Same content")
        self.assertNotEqual(post1, post2)
    
    def test_post_inequality_different_text(self):
        """Test that posts with different text are not equal."""
        post1 = Post(1, "Same Title", "Content one")
        post2 = Post(1, "Same Title", "Content two")
        self.assertNotEqual(post1, post2)
    
    def test_post_equality_with_non_post(self):
        """Test that a Post is not equal to a non-Post object."""
        post = Post(1, "Title", "Content")
        self.assertNotEqual(post, "not a post")
        self.assertNotEqual(post, None)
        self.assertNotEqual(post, 123)
    
    def test_post_update_method(self):
        """Test that update method changes content and updates timestamp."""
        post = Post(1, "Old Title", "Old content")
        original_created = post.created_at
        original_updated = post.updated_at
        
        # Wait a tiny bit to ensure timestamp difference
        import time
        time.sleep(0.001)
        
        # Update the post
        post.update("New Title", "New content")
        
        # Check content changed
        self.assertEqual(post.title, "New Title")
        self.assertEqual(post.text, "New content")
        
        # Check created_at unchanged but updated_at changed
        self.assertEqual(post.created_at, original_created)
        self.assertNotEqual(post.updated_at, original_updated)
        self.assertGreater(post.updated_at, original_updated)
    
    def test_post_string_representation(self):
        """Test the string representation of a Post."""
        post = Post(5, "My Blog Post", "Interesting content")
        
        # Test __str__ method
        str_representation = str(post)
        self.assertIn("Post #5", str_representation)
        self.assertIn("My Blog Post", str_representation)
        
        # Test __repr__ method
        repr_representation = repr(post)
        self.assertIn("Post(", repr_representation)
        self.assertIn("id=5", repr_representation)
        self.assertIn("title='My Blog Post'", repr_representation)
    
    def test_multiple_posts_unique_timestamps(self):
        """Test that multiple posts created in sequence have unique timestamps."""
        post1 = Post(1, "First Post", "Content one")
        import time
        time.sleep(0.001)  # Small delay
        post2 = Post(2, "Second Post", "Content two")
        
        # Each post should have its own creation timestamp
        self.assertNotEqual(post1.created_at, post2.created_at)
        self.assertLess(post1.created_at, post2.created_at)


if __name__ == '__main__':
    unittest.main()