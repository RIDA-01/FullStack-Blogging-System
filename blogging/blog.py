from blogging.dao.post_dao_pickle import PostDAOPickle
from blogging.post import Post

class Blog:
    def __init__(self, blog_id, name, url, email):
        self.blog_id = blog_id
        self.name = name
        self.url = url
        self.email = email
        # DAO responsible for managing this blog's posts (in memory + file).
        self.post_dao = PostDAOPickle(self)
        # Initialize post_counter based on existing posts (for persistence).
        if self.post_dao.posts:
            max_id = max(p.post_id for p in self.post_dao.posts)
            self.post_counter = max_id + 1
        else:
            self.post_counter = 1
    
    def __eq__(self, other):
        """ Compare two Blog objects for equality """
        if not isinstance(other, Blog):
            return False
        return (self.blog_id == other.blog_id and 
                self.name == other.name and
                self.url == other.url and
                self.email == other.email)
    
    def create_post(self, title, text): 
        """
        Create a new Post for this blog and return it
        """
        p = Post(self.post_counter, title, text)
        self.post_counter += 1 
        return self.post_dao.create_post(p)
    

    def search_post(self, post_id):
        """ 
        Find a specific post in this blog by its ID
        Delegate post search to the DAO 
        """
        return self.post_dao.search_post(post_id)

    def retrieve_posts(self, query):
        """
        Search for posts containing the query string in title or text.
        Case-insensitive search in title OR text, return ASC by code
        """
        return self.post_dao.retrieve_posts(query)


    def update_post(self, post_id, title, text):
        """
        Search through all posts to find the one with matching ID
        """
        # for p in self.posts:
        #     if p.post_id == post_id:
        #         p.update(title, text)  # Use Post's method to handle timestamps
        #         return True# Successfully updated
        # return False # # Return false if no post found with the given ID
        return self.post_dao.update_post(post_id, title, text)


    def delete_post(self, post_id):
        # for i, p in enumerate(self.posts):
        #     if p.post_id == post_id:
        #         del self.posts[i]
        #         return True 
        # return False #True if post was found and deleted, False otherwise
        return self.post_dao.delete_post(post_id)

    def list_posts(self):
        """
        """
        return self.post_dao.list_posts()


       
    def __str__(self):
        """String representation of the Blog"""
        return f"Blog(id={self.blog_id}, name='{self.name}', url='{self.url}')"
    
    def __repr__(self):
        """Detailed representation of the Blog"""
        return f"Blog(blog_id={self.blog_id}, name='{self.name}', url='{self.url}', email='{self.email}')"