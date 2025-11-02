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
    

       
    def __str__(self):
        """String representation of the Blog"""
        return f"Blog(id={self.blog_id}, name='{self.name}', url='{self.url}')"
    
    def __repr__(self):
        """Detailed representation of the Blog"""
        return f"Blog(blog_id={self.blog_id}, name='{self.name}', url='{self.url}', email='{self.email}')"