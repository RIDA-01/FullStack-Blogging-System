from blogging.dao.post_dao import PostDAO
from blogging.post import Post

class PostDAOPickle(PostDAO):
    def __init__(self, blog):
        self.blog = blog
        self.posts = []  # Store posts in memory
    
    def search_post(self, key):
        """Find a post by ID"""
        for post in self.posts:
            if post.post_id == key:
                return post
        return None
    
    def create_post(self, post):
        """Create a new post"""
        if self.search_post(post.post_id) is not None:
            return None
        
        self.posts.append(post)
        return post
    
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
            return None
        
        post.update(new_title, new_text)
        return post
    
    def delete_post(self, key):
        """Delete a post by ID"""
        for i, post in enumerate(self.posts):
            if post.post_id == key:
                del self.posts[i]
                return True
        return False
    
    def list_posts(self):
        """Get all posts sorted by ID descending"""
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)