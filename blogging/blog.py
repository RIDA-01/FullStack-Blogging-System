class Blog:
    def __init__(self, blog_id, name, url, email):
        self.blog_id = blog_id
        self.name = name
        self.url = url
        self.email = email
        self.posts = []  # For Yasaman's posts later
        self.post_counter = 1  # For auto-incrementing post IDs
    
    def __eq__(self, other):
       return False