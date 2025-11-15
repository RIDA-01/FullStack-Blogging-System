from blogging.blog import Blog
from blogging.post import Post
import hashlib
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:
    def __init__(self):
        self.current_user = None
        # Hardcoded user for now - from the test
        self.users = self.load_users()  # Load from file instead of hardcoding
        self.blogs = []  #store all Blog objects
        self.current_blog = None \
        
    def load_users(self):
        """Load users from users.txt file with username,password_hash format"""
        users = {}
        try:
            with open('blogging/users.txt', 'r') as file:
                for line in file:
                    # Remove any extra whitespace/newlines
                    cleaned_line = line.strip()
                    
                    # Skip empty lines
                    if not cleaned_line:
                        continue
                    
                    # Split by comma
                    parts = cleaned_line.split(',')
                    
                    if len(parts) == 2:
                        username = parts[0].strip()
                        password_hash = parts[1].strip()
                        users[username] = password_hash
                        
        except FileNotFoundError:
            print("users.txt file not found")
        except Exception as e:
            print(f"Error reading users.txt: {e}")
        return users
    
    def get_password_hash(self, password):
        """Convert password to SHA-256 hash"""
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def login(self, username, password):#story 1    
        if self.current_user is not None:#checking if already logged in
            raise DuplicateLoginException()  # Already logged in
            
         # Check if username exists and password hash matches
        if username in self.users:
            password_hash = self.get_password_hash(password)
            if self.users[username] == password_hash:
                self.current_user = username
                return True
        raise InvalidLoginException()  # Wrong credentials
    
    def logout(self):#story2
        if self.current_user is not None:#if logged in then u can log out
            self.current_user = None
            self.current_blog = None #added this line for story 9
            return True
        raise InvalidLogoutException()  # Not logged in
    
    def create_blog(self, blog_id, name, url, email):#story 3

        if self.current_user is None:   #checking if already logged in
            raise IllegalAccessException()

        #checking if blog_id already exists
        for blog in self.blogs:
            if blog.blog_id == blog_id:
                 raise IllegalOperationException()  # Exception instead of None

        #Creating new blog and adding to collection
        new_blog = Blog(blog_id, name, url, email)
        self.blogs.append(new_blog)
        return new_blog
        
    def search_blog(self, blog_id):#story 4
        
        if self.current_user is None: #checking if already logged in
            raise IllegalAccessException()  # Exception instead of None
        
        #search for blog by ID
        for blog in self.blogs:
            if blog.blog_id == blog_id:
                return blog
        
        return None  #when its not found return nothing
    
    def retrieve_blogs(self, name):#stroy 5

        if self.current_user is None: #checking if already logged in
            raise IllegalAccessException()
        
        #searching for blogs that contain the name substring
        matching_blogs = []
        for blog in self.blogs:
            if name in blog.name:  # Partial match
                matching_blogs.append(blog)
        
        return matching_blogs
    
    def update_blog(self, old_id, new_id, name, url, email): #story 6

        if self.current_user is None: #checking if already logged in
            raise IllegalAccessException()
        
         #checkinng to delete the current blog
        if self.current_blog and self.current_blog.blog_id == old_id:
            raise IllegalOperationException()  # Can't update current blog
        
        #finding the blog to update
        blog_to_update = None
        for blog in self.blogs:
            if blog.blog_id == old_id:
                blog_to_update = blog
                break
        
        #if it didn't find any blog then return false
        if blog_to_update is None:
            raise IllegalOperationException()  # Exception instead of False
        
        #checking if new_id conflicts with existing blogs
        if old_id != new_id:  #only check if ID is changing
            for blog in self.blogs:
                if blog.blog_id == new_id and blog != blog_to_update: #except the one we're updating
                     raise IllegalOperationException()  # Exception instead of False  #new ID already exists
        
        #update the blog attributes
        blog_to_update.blog_id = new_id
        blog_to_update.name = name
        blog_to_update.url = url
        blog_to_update.email = email
        
        return True
    

    def delete_blog(self, blog_id): #story 7

        if self.current_user is None: #checking if already logged in
            raise IllegalAccessException()
        
        #checkinng to delete the current blog
        if self.current_blog and self.current_blog.blog_id == blog_id:
            raise IllegalOperationException()  # Can't update current blog  #can't delete current blog
        
        #finding the blog to delete
        for i, blog in enumerate(self.blogs):
            if blog.blog_id == blog_id:
                #remove the blog from the list
                del self.blogs[i]
                return True
            
          #if it didn't find any blog then return false
        raise IllegalOperationException()  # Exception instead of False
        
    def list_blogs(self): #story 8

        if self.current_user is None:  #checking if already logged in
            raise IllegalAccessException()
        
        #return a copy of the blogs list
        return self.blogs

    def set_current_blog(self, blog_id): #story 9
        if self.current_user is None:
            raise IllegalAccessException()  # Added login check at start
        #finding the blog by ID
        blog = self.search_blog(blog_id)  #use the search from story 4
        if blog is not None:
            self.current_blog = blog
            return True
        raise IllegalOperationException()  # Exception instead of False

    def get_current_blog(self):
        if self.current_user is None:
            raise IllegalAccessException()  # Added login check
        return self.current_blog

    def unset_current_blog(self):
        if self.current_user is None:
            raise IllegalAccessException()  # Added login check
        self.current_blog = None
        return True
    
    """
    Post functions:
    """
    def create_post(self, title: str, text: str): #story 10
        #Must be logged in and have a current blog selected
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
    
    # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
            return None
        # # Delegate to current blog's create_post method
        return blog.create_post(title, text) #The newly created post, or None if requirements not met
    
    def search_post(self, post_id: int):
        ## Must be logged in and have a current blog selected
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
            return None
        return blog.search_post(post_id) #The found post, or None if not found or requirements not met


    def retrieve_posts(self, query: str): #story 11
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
          return None
        return blog.retrieve_posts(query)#Matching posts sorted by ID, or None if requirements not met
    

    def update_post(self, post_id: int, title: str, text: str): #story 12
         # Must be logged in and have a current blog selected
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
            return False
        return blog.update_post(post_id, title, text) #True if post was updated, False otherwise

    def delete_post(self, post_id: int): #story 13
        # Must be logged in and have a current blog selected
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
            return False
        return blog.delete_post(post_id) #True if post was deleted, False otherwise

    def list_posts(self): #story 14
         # Must be logged in and have a current blog selected
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
            return None
        return blog.list_posts() #All posts sorted by ID descending, or None if requirements not met