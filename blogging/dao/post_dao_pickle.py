import os
import pickle
from blogging.dao.post_dao import PostDAO
from blogging.post import Post
from blogging.configuration import Configuration 

class PostDAOPickle(PostDAO):
    def __init__(self, blog):
        self.blog = blog
        self.autosave = Configuration.autosave  # FIX: Direct class access
        
        # Use Configuration for file paths
        records_dir = os.path.join("blogging", Configuration.records_path)
        os.makedirs(records_dir, exist_ok=True)
        
        self.filename = os.path.join(records_dir, f"{blog.blog_id}{Configuration.records_extension}")
        
        if self.autosave:
            try:
                with open(self.filename, "rb") as f:
                    self.posts = pickle.load(f)
                    # Update blog's post counter after loading
                    if self.posts:
                        max_id = max(post.post_id for post in self.posts)
                        self.blog.post_counter = max_id + 1
            except FileNotFoundError:
                self.posts = []
        else:
            self.posts = []
    
    def search_post(self, key):
        for post in self.posts:
            if post.post_id == key:
                return post
        return None
    
    def create_post(self, post):
        if self.search_post(post.post_id) is not None:
            return None
        
        self.posts.append(post)
        
        # Update blog's post counter
        if post.post_id >= self.blog.post_counter:
            self.blog.post_counter = post.post_id + 1
            
        self._save_if_autosave()
        return post
    
    def retrieve_posts(self, search_string):
        q = (search_string or "").lower()
        matches = []
        for post in self.posts:
            if (q in post.title.lower() or 
                q in post.text.lower()):
                matches.append(post)
        return sorted(matches, key=lambda p: p.post_id)
    
    def update_post(self, key, new_title, new_text):
        post = self.search_post(key)
        if post is None:
            return False
        
        post.update(new_title, new_text)
        self._save_if_autosave()
        return True
    
    def delete_post(self, key):
        for i, post in enumerate(self.posts):
            if post.post_id == key:
                del self.posts[i]
                self._save_if_autosave()
                return True
        return False
    
    def list_posts(self):
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)
    
    def _save_if_autosave(self):
        if self.autosave:
            with open(self.filename, "wb") as f:
                pickle.dump(self.posts, f)