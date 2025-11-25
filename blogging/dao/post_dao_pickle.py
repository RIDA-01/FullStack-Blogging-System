import os
import pickle
from blogging.dao.post_dao import PostDAO
from blogging.post import Post
from blogging.configuration import Configuration 

class PostDAOPickle(PostDAO):
    def __init__(self, blog):
        # DAO is tied to a specific Blog object
        self.blog = blog
        # we look into changes should automatically be written to disk
        self.autosave = Configuration.autosave
        records_dir = Configuration.records_path   # all post records are stored
        os.makedirs(records_dir, exist_ok=True)

        # path to the pickle file for this specific blog's posts
        self.filename = os.path.join(
            records_dir, 
            f"{blog.blog_id}{Configuration.records_extension}"
        )

        #loading posts from disk if autosave is enabled
        if self.autosave:
            try:
                with open(self.filename, "rb") as f: #same as lab9
                    self.posts = pickle.load(f)
            except FileNotFoundError:
                # if no file exists then we will start empty
                self.posts = []
        else:
            # in no autosave then always start empty
            self.posts = []

        # ensure blog.post_counter is correct after loading
        if self.posts:
            # highest post_id + 1 becomes next ID for new posts
            max_id = max(post.post_id for post in self.posts)
            self.blog.post_counter = max_id + 1
        else:
            # initialize if missing
            if not hasattr(self.blog, "post_counter"):
                self.blog.post_counter = 1
    
    def search_post(self, key): # return the post with matching post_id  or None
        for post in self.posts:
            if post.post_id == key:
                return post
        return None
    
    def create_post(self, post):# add a new post unless a post with the same ID already exists
        if self.search_post(post.post_id) is not None:
            return None
        
        self.posts.append(post)

        # ensure the blog’s post counter is always ahead of the highest ID
        if post.post_id >= self.blog.post_counter:
            self.blog.post_counter = post.post_id + 1

        self._save_if_autosave()
        return post
    
    def retrieve_posts(self, search_string):
        """
        Return posts where the search string appears in 
        either the title or text (case-insensitive), sorted by post_id.
        """
        q = (search_string or "").lower()
        matches = []
        
        for post in self.posts:
            if (q in post.title.lower() or q in post.text.lower()):
                matches.append(post)
        
        return sorted(matches, key=lambda p: p.post_id)
    
    def update_post(self, key, new_title, new_text): # update the title and text of a post if it exists
        post = self.search_post(key)
        if post is None:
            return False
        
        post.update(new_title, new_text)
        self._save_if_autosave()
        return True
    
    def delete_post(self, key): # Delete a post by ID if it exists."""
        for i, post in enumerate(self.posts):
            if post.post_id == key:
                del self.posts[i]
                self._save_if_autosave()
                return True
        return False
    
    def list_posts(self): # Return posts ordered from newest to oldest
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)
    

    
    def _save_if_autosave(self): # Write posts to the pickle file when autosave=True
        if self.autosave:
            with open(self.filename, "wb") as f:
                pickle.dump(self.posts, f)
