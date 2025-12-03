from blogging.dao.post_dao_pickle import PostDAOPickle
from blogging.post import Post

class Blog:
    def __init__(self, blog_id, name, url, email):
        # Basic blog information
        self.blog_id = blog_id
        self.name = name
        self.url = url
        self.email = email

        # default value for new blogs
        self.post_counter = 1

        # DAO responsible for managing this blog's posts (in memory + file).
        # If there are existing posts on disk, DAO will update post_counter.
        self.post_dao = PostDAOPickle(self)
    
    # CLI expects blog.id
    @property
    def id(self):
        return self.blog_id

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
        Create a new Post for this blog then save the post through the DAO
        """
        p = Post(self.post_counter, title, text)
        self.post_counter += 1 
        return self.post_dao.create_post(p)
    

    def search_post(self, post_id):
        """ 
        Ask DAO to find a post by ID.
        Blog itself does not search inside the list
        """
        return self.post_dao.search_post(post_id)

    def retrieve_posts(self, query):
        """
        Ask DAO to return posts matching the search text
        Search is case insensitive and checks both title and text
        """
        return self.post_dao.retrieve_posts(query)


    def update_post(self, post_id, title, text):
        """
        Ask DAO to update a post with new title/text.
        """
        return self.post_dao.update_post(post_id, title, text)


    def delete_post(self, post_id):
        """
        Delete a post using the DAO
        """
        return self.post_dao.delete_post(post_id)

    def list_posts(self):
        """
        Return all posts sorted by ID (descending)
        DAO does the sorting logic
        """
        return self.post_dao.list_posts()


       
    def __str__(self):
        """String representation of the Blog"""
        return f"Blog(id={self.blog_id}, name='{self.name}', url='{self.url}')"
    
    def __repr__(self):
        """Detailed representation of the Blog"""
        return f"Blog(blog_id={self.blog_id}, name='{self.name}', url='{self.url}', email='{self.email}')"