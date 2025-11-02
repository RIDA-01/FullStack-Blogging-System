"""
    I added this Line !
"""
from blogging.post import Post


class Blog:
    def __init__(self, blog_id, name, url, email):
        self.blog_id = blog_id
        self.name = name
        self.url = url
        self.email = email
        self.posts = []  # For Yasaman's posts later
        self.post_counter = 1  # For auto-incrementing post IDs
    
    def __eq__(self, other):
       # Compare two Blog objects for equality
        if not isinstance(other, Blog):
            return False
        return (self.blog_id == other.blog_id and 
                self.name == other.name and
                self.url == other.url and
                self.email == other.email)
    

    """
    Functions I added to Blog file:
    """
    def create_post(self, title, text):
        # Codes start at 1 and auto-increment per blog
        p = Post(self.post_counter, title, text)
        self.posts.append(p)
        self.post_counter += 1
        return p

    def search_post(self, post_id):
        for p in self.posts:
            if p.post_id == post_id:
                return p
        return None

    def retrieve_posts(self, query):
        # Case-insensitive search in title OR text, return ASC by code
        q = (query or "").lower()
        matches = []
        for p in self.posts:
            if q in p.title.lower() or q in p.text.lower():
                matches.append(p)
        return sorted(matches, key=lambda p: p.post_id)  # ascending

    def update_post(self, post_id, title, text):
        for p in self.posts:
            if p.post_id == post_id:
                p.title = title
                p.text = text
                return True
        return False

    def delete_post(self, post_id):
        for i, p in enumerate(self.posts):
            if p.post_id == post_id:
                del self.posts[i]
                return True
        return False

    def list_posts(self):
        # Return DESC by code
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)
    

    """
    END
    """

       
    def __str__(self):
        """String representation of the Blog"""
        return f"Blog(id={self.blog_id}, name='{self.name}', url='{self.url}')"
    
    def __repr__(self):
        """Detailed representation of the Blog"""
        return f"Blog(blog_id={self.blog_id}, name='{self.name}', url='{self.url}', email='{self.email}')"