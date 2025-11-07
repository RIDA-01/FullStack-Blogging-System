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
    
    def create_post(self, title, text): #text (str): The content of the post
        # Codes start at 1 and auto-increment per blog
        p = Post(self.post_counter, title, text)
        self.posts.append(p)
        self.post_counter += 1 
        return p  # Returns: Post: The newly created Post object
    

    def search_post(self, post_id): #Find a specific post in this blog by its ID.
        for p in self.posts:
            if p.post_id == post_id:
                return p
        return None #The found post object, or None if not found

    def retrieve_posts(self, query): # Search for posts containing the query string in title or text.
        # Case-insensitive search in title OR text, return ASC by code
        q = (query or "").lower()
        matches = []
        for p in self.posts:
            if q in p.title.lower() or q in p.text.lower():
                matches.append(p)
        return sorted(matches, key=lambda p: p.post_id)  # List of Post objects matching the query, sorted by post ID ascending

    def update_post(self, post_id, title, text):
        # # Search through all posts to find the one with matching ID
        for p in self.posts:
            if p.post_id == post_id:
                p.update(title, text)  # Use Post's method to handle timestamps
                return True# Successfully updated
        return False # # Return false if no post found with the given ID

    def delete_post(self, post_id):
        for i, p in enumerate(self.posts):
            if p.post_id == post_id:
                del self.posts[i]
                return True 
        return False #True if post was found and deleted, False otherwise

    def list_posts(self):
        # Return DESC by code
        return sorted(self.posts, key=lambda p: p.post_id, reverse=True)

       
    def __str__(self):
        """String representation of the Blog"""
        return f"Blog(id={self.blog_id}, name='{self.name}', url='{self.url}')"
    
    def __repr__(self):
        """Detailed representation of the Blog"""
        return f"Blog(blog_id={self.blog_id}, name='{self.name}', url='{self.url}', email='{self.email}')"