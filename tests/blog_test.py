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

if __name__ == '__main__':
    unittest.main()