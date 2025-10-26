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
        
    def search_blog(self, blog_id):#story 4
        
        if self.current_user is None: #checking if already logged in
            return None
        
        #search for blog by ID
        for blog in self.blogs:
            if blog.blog_id == blog_id:
                return blog
        
        return None  #when its not found return nothing
    
    def retrieve_blogs(self, name):#stroy 5

        if self.current_user is None: #checking if already logged in
            return None
        
        #searching for blogs that contain the name substring
        matching_blogs = []
        for blog in self.blogs:
            if name in blog.name:  # Partial match
                matching_blogs.append(blog)
        
        return matching_blogs
    
    def update_blog(self, old_id, new_id, name, url, email): #story 6

        if self.current_user is None: #checking if already logged in
            return False
        
        #finding the blog to update
        blog_to_update = None
        for blog in self.blogs:
            if blog.blog_id == old_id:
                blog_to_update = blog
                break
        
        #if it didn't find any blog then return false
        if blog_to_update is None:
            return False
        
        #checking if new_id conflicts with existing blogs
        if old_id != new_id:  #only check if ID is changing
            for blog in self.blogs:
                if blog.blog_id == new_id and blog != blog_to_update: #except the one we're updating
                    return False  #new ID already exists
        
        #update the blog attributes
        blog_to_update.blog_id = new_id
        blog_to_update.name = name
        blog_to_update.url = url
        blog_to_update.email = email
        
        return True