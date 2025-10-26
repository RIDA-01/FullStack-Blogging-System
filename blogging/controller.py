from blogging.blog import Blog


class Controller:
    def __init__(self):
        self.current_user = None
        # Hardcoded user for now - from the test
        self.users = {"user": "blogging2025"}#story1,2
        self.blogs = []  #store all Blog objects
        self.current_blog = None 
    
    def login(self, username, password):#story 1    
        if self.current_user is not None:#checking if already logged in
            return False
            
        if username in self.users and self.users[username] == password: #checking username exists and password matche
            self.current_user = username
            return True
        return False
    
    def logout(self):#story2
        if self.current_user is not None:#if logged in then u can log out
            self.current_user = None
            return True
        return False
    
    def create_blog(self, blog_id, name, url, email):#story 3

        if self.current_user is None:   #checking if already logged in
            return None

        #checking if blog_id already exists
        for blog in self.blogs:
            if blog.blog_id == blog_id:
                return None  # Blog ID already exists

        #Creating new blog and adding to collection
        new_blog = Blog(blog_id, name, url, email)
        self.blogs.append(new_blog)
        return new_blog
        
  