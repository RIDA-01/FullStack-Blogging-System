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
        self._loaded = False
        
        if self.autosave:
            self._load_blogs()
            self._loaded = True
        
    def _ensure_loaded(self):
        if self.autosave and not self._loaded:
            self._load_blogs()
            self._loaded = True


        
    def _save_blogs(self):
        """Save blogs to JSON file"""
        if not self.autosave:
            return
            
        try:
            blogs_file = os.path.join("blogging", Configuration.blogs_file)
            print(f"DEBUG _save_blogs: Saving {len(self.blogs)} blogs to {blogs_file}")
            
            os.makedirs(os.path.dirname(blogs_file), exist_ok=True)
            
            with open(blogs_file, 'w') as file:
                blogs_list = list(self.blogs.values())
                print(f"DEBUG _save_blogs: Saving blogs: {[b.blog_id for b in blogs_list]}")
                json.dump(blogs_list, file, cls=BlogEncoder, indent=2)
            print(f"DEBUG _save_blogs: Successfully saved to file")
        except Exception as e:
            print(f"Error saving blogs to file: {e}")

    def _load_blogs(self):
        """Load blogs from JSON file - only called when autosave=True"""
        try:
            blogs_file = os.path.join("blogging", Configuration.blogs_file)
            print(f"DEBUG _load_blogs: Loading from {blogs_file}, exists: {os.path.exists(blogs_file)}")
            
            if os.path.exists(blogs_file):
                with open(blogs_file, 'r') as file:
                    blogs_list = json.load(file, cls=BlogDecoder)
                    print(f"DEBUG _load_blogs: Loaded blogs: {blogs_list}")
                    self.blogs = {blog.blog_id: blog for blog in blogs_list}
                    print(f"DEBUG _load_blogs: Successfully loaded {len(self.blogs)} blogs")
            else:
                self.blogs = {}
                print("DEBUG _load_blogs: File doesn't exist, starting empty")
        except Exception as e:
            print(f"Error loading blogs from file: {e}")
            self.blogs = {}
    
        # Update ALL methods to call _ensure_loaded first:
    def create_blog(self, blog):
        self._ensure_loaded()
        print(f"DEBUG BlogDAOJSON.create_blog: Creating blog {blog.blog_id}, current blogs: {list(self.blogs.keys())}")
        
        if blog.blog_id in self.blogs:
            print("Blog ID already exists")
            return None
        
        self.blogs[blog.blog_id] = blog
        print(f"DEBUG BlogDAOJSON.create_blog: Blog created. Total blogs: {len(self.blogs)}, keys: {list(self.blogs.keys())}")
        self._save_blogs()
        return blog

    def search_blog(self, key):
        self._ensure_loaded()
        print(f"DEBUG BlogDAOJSON.search_blog: Looking for {key}, available blogs: {list(self.blogs.keys())}")
        result = self.blogs.get(key)
        print(f"DEBUG BlogDAOJSON.search_blog: Returning: {result}")
        return result

    def _ensure_loaded(self):
        print(f"DEBUG BlogDAOJSON._ensure_loaded: autosave={self.autosave}, _loaded={getattr(self, '_loaded', False)}")
        if self.autosave and not getattr(self, '_loaded', False):
            self._load_blogs()
            self._loaded = True
            
            if blog.blog_id in self.blogs:
                print("Blog ID already exists")
                return None
            
            self.blogs[blog.blog_id] = blog
            print(f"Blog created successfully. Total blogs: {len(self.blogs)}")
            self._save_blogs()
            return blog
        
    def retrieve_blogs(self, search_string):
        self._ensure_loaded()
        matching_blogs = []
        for blog in self.blogs.values():
            if search_string.lower() in blog.name.lower():
                matching_blogs.append(blog)
        return matching_blogs
    
    def update_blog(self, key, blog):
        self._ensure_loaded()
        if key not in self.blogs:
            return None
        
        if key != blog.blog_id:
            del self.blogs[key]
        
        self.blogs[blog.blog_id] = blog
        self._save_blogs()
        return blog
    
    def delete_blog(self, key):
        self._ensure_loaded()
        if key in self.blogs:
            del self.blogs[key]
            self._save_blogs()
            return True
        return False
    
    def list_blogs(self):
        self._ensure_loaded()
        return list(self.blogs.values())