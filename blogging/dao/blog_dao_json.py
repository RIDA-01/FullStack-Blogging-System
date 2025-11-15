from blogging.dao.blog_dao import BlogDAO
from blogging.blog import Blog
import json

class BlogDAOJSON(BlogDAO):
     
    def __init__(self):
        self.blogs = {}  # Use dictionary for blog storage
    
    def search_blog(self, key):
        """Find a blog by ID"""
        return self.blogs.get(key)
    
    def create_blog(self, blog):
        """Create a new blog"""
        # Check if blog ID already exists
        if blog.blog_id in self.blogs:
            return None
        
        self.blogs[blog.blog_id] = blog
        return blog
    
    def retrieve_blogs(self, search_string):
        """Search blogs by name substring"""
        matching_blogs = []
        for blog in self.blogs.values():
            if search_string.lower() in blog.name.lower():
                matching_blogs.append(blog)
        return matching_blogs
    
    def update_blog(self, key, blog):
        """Update a blog"""
        if key not in self.blogs:
            return None
       # If the key is changing, we need to remove the old entry
        if key != blog.blog_id:
            del self.blogs[key]
    
        # Add the blog with the new key
        self.blogs[blog.blog_id] = blog
        return blog 
    
    def delete_blog(self, key):
        """Delete a blog by ID"""
        if key in self.blogs:
            del self.blogs[key]
            return True
        return False
    
    def list_blogs(self):
        """Get all blogs"""
        return list(self.blogs.values())