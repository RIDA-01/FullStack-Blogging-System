import unittest
from blogging.blog import Blog

class TestBlog(unittest.TestCase):
    
    def test_blog_creation(self):
        #test that a Blog object is created with correct attributes
        blog = Blog(123, "Test Blog", "test_url", "test@email.com")
        self.assertEqual(blog.blog_id, 123)
        self.assertEqual(blog.name, "Test Blog")
        self.assertEqual(blog.url, "test_url")
        self.assertEqual(blog.email, "test@email.com")
    
    def test_blog_equality(self):
        #Test of two equal Blog objects
        blog1 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        blog2 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        self.assertEqual(blog1, blog2)
    
    def test_blog_inequality(self):
        #Test of two different Blog objects
        blog1 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        blog2 = Blog(222, "Yasaman Rezapour", "yasaman_rezapour", "yrezapour@uvic.ca")
        self.assertNotEqual(blog1, blog2)

    def test_create_post(self):
        """Test creating a new post in the blog."""
        post = self.blog.create_post("Test Title", "Test Content")
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.text, "Test Content")
        self.assertEqual(post.post_id, 1)  # First post should have ID 1
    
    def test_search_post_found(self):
        """Test searching for an existing post."""
        post = self.blog.create_post("Find Me", "Searchable content")
        found_post = self.blog.search_post(1)
        self.assertEqual(post, found_post)
    
    def test_search_post_not_found(self):
        """Test searching for a non-existent post returns None."""
        found_post = self.blog.search_post(999)
        self.assertIsNone(found_post)
    
    def test_retrieve_posts_with_query(self):
        """Test retrieving posts by search query."""
        self.blog.create_post("Python Tutorial", "Learn Python programming")
        self.blog.create_post("Java Guide", "Java programming guide")
        
        # Search for "Python" should return one post
        results = self.blog.retrieve_posts("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Tutorial")
    
    def test_update_post_success(self):
        """Test successfully updating a post."""
        self.blog.create_post("Old Title", "Old Content")
        success = self.blog.update_post(1, "New Title", "New Content")
        self.assertTrue(success)
        
        updated_post = self.blog.search_post(1)
        self.assertEqual(updated_post.title, "New Title")
        self.assertEqual(updated_post.text, "New Content")
    
    def test_update_post_not_found(self):
        """Test updating a non-existent post returns False."""
        success = self.blog.update_post(999, "Title", "Content")
        self.assertFalse(success)
    
    def test_delete_post_success(self):
        """Test successfully deleting a post."""
        self.blog.create_post("To Delete", "Content")
        success = self.blog.delete_post(1)
        self.assertTrue(success)
        self.assertIsNone(self.blog.search_post(1))
    
    def test_list_posts_order(self):
        """Test that list_posts returns posts in descending ID order."""
        self.blog.create_post("First", "Content 1")
        self.blog.create_post("Second", "Content 2")
        
        posts = self.blog.list_posts()
        self.assertEqual(posts[0].post_id, 2)  # Most recent first
        self.assertEqual(posts[1].post_id, 1)  # Older post last

    
if __name__ == '__main__':
    unittest.main()