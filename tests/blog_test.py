import unittest
from blogging.blog import Blog

class TestBlog(unittest.TestCase):
    def setUp(self):
        # create a fresh blog for each test so IDs start at 1
        self.blog = Blog(123, "Test Blog", "test_url", "test@email.com")
    
    def test_blog_creation(self):
        blog = Blog(123, "Test Blog", "test_url", "test@email.com")
        self.assertEqual(blog.blog_id, 123)
        self.assertEqual(blog.name, "Test Blog")
        self.assertEqual(blog.url, "test_url")
        self.assertEqual(blog.email, "test@email.com")
    
    def test_blog_equality(self):
        blog1 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        blog2 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        self.assertEqual(blog1, blog2)
    
    def test_blog_inequality(self):
        blog1 = Blog(111, "Rida Deeb", "rida_deeb", "rida1@uvic.ca")
        blog2 = Blog(222, "Yasaman Rezapour", "yasaman_rezapour", "yrezapour@uvic.ca")
        self.assertNotEqual(blog1, blog2)

    def test_create_post(self):
        post = self.blog.create_post("Test Title", "Test Content")
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.text, "Test Content")
        self.assertEqual(post.post_id, 1)
    
    def test_search_post_found(self):
        post = self.blog.create_post("Find Me", "Searchable content")
        found_post = self.blog.search_post(1)
        self.assertEqual(post, found_post)
    
    def test_search_post_not_found(self):
        found_post = self.blog.search_post(999)
        self.assertIsNone(found_post)
    
    def test_retrieve_posts_with_query(self):
        self.blog.create_post("Python Tutorial", "Learn Python programming")
        self.blog.create_post("Java Guide", "Java programming guide")
        results = self.blog.retrieve_posts("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Tutorial")
    
    def test_update_post_success(self):
        self.blog.create_post("Old Title", "Old Content")
        success = self.blog.update_post(1, "New Title", "New Content")
        self.assertTrue(success)
        updated_post = self.blog.search_post(1)
        self.assertEqual(updated_post.title, "New Title")
        self.assertEqual(updated_post.text, "New Content")
    
    def test_update_post_not_found(self):
        success = self.blog.update_post(999, "Title", "Content")
        self.assertFalse(success)
    
    def test_delete_post_success(self):
        self.blog.create_post("To Delete", "Content")
        success = self.blog.delete_post(1)
        self.assertTrue(success)
        self.assertIsNone(self.blog.search_post(1))
    
    def test_list_posts_order(self):
        self.blog.create_post("First", "Content 1")
        self.blog.create_post("Second", "Content 2")
        posts = self.blog.list_posts()
        self.assertEqual(posts[0].post_id, 2)  # newest first
        self.assertEqual(posts[1].post_id, 1)

if __name__ == '__main__':
    unittest.main()
