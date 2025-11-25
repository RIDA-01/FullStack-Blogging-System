from blogging.dao.blog_dao import BlogDAO
from blogging.blog import Blog
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder
from blogging.configuration import Configuration
import json
import os

class BlogDAOJSON(BlogDAO):
    def __init__(self, autosave=False):
        self.blogs = {}
        self.autosave = autosave
        self._loaded = False #track if the file data is loaded

        #if autosave=True then we will load existing blogs
        if self.autosave:
            self._load_blogs()
            self._loaded = True

    def _get_blogs_file(self):
        # address blogs.json
        return Configuration.blogs_file 

    def _ensure_loaded(self): #loads blogs from file only once
        if self.autosave and not self._loaded:
            self._load_blogs()
            self._loaded = True

        
    def _save_blogs(self):
        """Save blogs to JSON file"""
        if not self.autosave:
            return
            
        try:
            blogs_file = self._get_blogs_file()
            os.makedirs(os.path.dirname(blogs_file) or ".", exist_ok=True) #create directory if needed
            #convert blogs to a list and write JSON
            blogs_list = list(self.blogs.values())
            with open(blogs_file, "w") as f:
                json.dump(blogs_list, f, cls=BlogEncoder, indent=2)
        except Exception as e:
            print(f"Error saving blogs to file: {e}")

    def _load_blogs(self):
        """Load blogs from JSON file - only called when autosave=True"""
        try:
            blogs_file = self._get_blogs_file()
            
            if os.path.exists(blogs_file):
                with open(blogs_file, 'r') as file:
                    blogs_list = json.load(file, cls=BlogDecoder)
                self.blogs = {blog.blog_id: blog for blog in blogs_list} #rebuild dictionary: {blog_id: Blog}
            else:
                self.blogs = {}
        except Exception as e:
            print(f"Error loading blogs from file: {e}")
            self.blogs = {}
    
  
    def create_blog(self, blog):
        self._ensure_loaded()
        
        if blog.blog_id in self.blogs: #we did this to avoid duplicates
            print("Blog ID already exists")
            return None
        
        self.blogs[blog.blog_id] = blog
        self._save_blogs()
        return blog

    def search_blog(self, key):
         #return blog with exact blog_id
        self._ensure_loaded()
        result = self.blogs.get(key)
        return result
    
    def retrieve_blogs(self, search_string):
        """we will return all blogs where the search string appears in the blog name """
        self._ensure_loaded()
        matching_blogs = []
        for blog in self.blogs.values():
            if search_string.lower() in blog.name.lower():
                matching_blogs.append(blog)
        return matching_blogs
    
    def update_blog(self, key, blog):
        """key = old_id
        blog.blog_id = new_id"""
        self._ensure_loaded()
        if key not in self.blogs:
            return None
        
        if key != blog.blog_id:   #if the ID changed remove old entry
            del self.blogs[key]
        
        self.blogs[blog.blog_id] = blog
        self._save_blogs()
        return blog
    
    def delete_blog(self, key):   #remove a blog by ID
        self._ensure_loaded()
        if key in self.blogs:
            del self.blogs[key]
            self._save_blogs()
            return True
        return False
    
    def list_blogs(self):  #returns a list of all Blog objects
        self._ensure_loaded()
        return list(self.blogs.values())