import os
import pickle
from blogging.dao.post_dao import PostDAO
from blogging.post import Post
from blogging.configuration import Configuration 

class PostDAOPickle(PostDAO):
    def __init__(self, blog):
        self.blog = blog
        conf = Configuration()
        self.autosave = conf.__class__.autosave
        # Directory where all post records for blogs will be stored
        records_dir = os.path.join("blogging", "records")
        os.makedirs(records_dir, exist_ok=True)
        # Build the full file path for this blog's post storage file.
        self.filename = os.path.join(records_dir, f"{blog.blog_id}.dat")
        if self.autosave:
            try:
                with open(self.filename, "rb") as f:
                    self.posts = pickle.load(f)
            except FileNotFoundError:
                self.posts = []
        else:
            self.posts = []

    
    def search_post(self, key):
        """Find a post by ID, return the Post or None"""
        for post in self.posts:
            if post.post_id == key:
                return post
        return None
    
    def create_post(self, post):
        """Create a new post"""
        if self.search_post(post.post_id) is not None:
            return False
        
        self.posts.append(post)
        self._save_if_autosave()
        return True
    
    def retrieve_posts(self, search_string):
        """Search posts by title or content substring"""
        q = (search_string or "").lower()
        matches = []
        for post in self.posts:
            if (q in post.title.lower() or 
                q in post.text.lower()):
                matches.append(post)
        return sorted(matches, key=lambda p: p.post_id)
    
    def update_post(self, key, new_title, new_text):
        """Update a post"""
        post = self.search_post(key)
        if post is None:
            return False
        
        post.update(new_title, new_text)
        self._save_if_autosave()
        return True
    
    def delete_post(self, key):
        """Delete a post by ID"""
        for i, post in enumerate(self.posts):
            if post.post_id == key:
                del self.posts[i]
                self._save_if_autosave()
                return True
        return False
    
    def list_posts(self):
        """Get all posts sorted by ID descending"""
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)
    

    def _save_if_autosave(self):
        """ Save posts to file only when autosave is enabled """
        if self.autosave:
            with open(self.filename, "wb") as f:
                pickle.dump(self.posts, f)
