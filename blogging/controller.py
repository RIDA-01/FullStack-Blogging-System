from blogging.blog import Blog
from blogging.post import Post
import hashlib
from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.configuration import Configuration 
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:
    def __init__(self, autosave=None):  # Make parameter optional
        self.current_user = None
        
        # If no autosave parameter provided, use Configuration.autosave
        if autosave is None:
            self.autosave = Configuration.autosave
        else:
            self.autosave = autosave
            
        self.users = self.load_users()
        self.blog_dao = BlogDAOJSON(self.autosave)  # Pass the actual autosave value
        self.current_blog = None
        
    def load_users(self):
        """Load users from users.txt file"""
        users = {}
        
        try:
            # Always try to load from file, regardless of autosave
            with open('blogging/users.txt', 'r') as file:
                for line in file:
                    # Remove any extra whitespace/newlines
                    cleaned_line = line.strip()
                    
                    # Skip empty lines
                    if not cleaned_line:
                        continue
                    
                    # Split by comma: username,password_hash
                    parts = cleaned_line.split(',')
                    
                    if len(parts) == 2:
                        username = parts[0].strip()
                        password_hash = parts[1].strip()
                        users[username] = password_hash
                        
        except FileNotFoundError:
            print("users.txt file not found - using empty user list")
        except Exception as e:
            print(f"Error reading users.txt: {e}")
        
        return users
    
    def get_password_hash(self, password):
        """ Convert password to SHA-256 hash """
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def login(self, username, password): # story 1    
        if self.current_user is not None: # check if already logged in
            raise DuplicateLoginException()  # Already logged in
            
         # Check if username exists and password hash matches
        if username in self.users:
            password_hash = self.get_password_hash(password)
            if self.users[username] == password_hash:
                self.current_user = username
                return True
        raise InvalidLoginException()  # Wrong credentials
    
    def logout(self):#story2
        if self.current_user is not None: # if logged in then u can log out
            self.current_user = None
            self.current_blog = None # added this line for story 9
            return True
        raise InvalidLogoutException()  # Not logged in
    
    def create_blog(self, blog_id, name, url, email):#story 3

        if self.current_user is None:   # check if already logged in
            raise IllegalAccessException()

         
        # Create Blog object first, then delegate to DAO
        new_blog = Blog(blog_id, name, url, email)
        result = self.blog_dao.create_blog(new_blog)
    
        if result is None:
            raise IllegalOperationException()  # Blog ID already exists
    
        return result
        
    def search_blog(self, blog_id):
        if self.current_user is None:
            raise IllegalAccessException()
        # we used the two commented lines debigging becuase we had errors adn we didnt know where they were
        # print(f"DEBUG search_blog: Looking for blog {blog_id}")
        result = self.blog_dao.search_blog(blog_id)
        # print(f"DEBUG search_blog: DAO returned: {result}")
        return result
    
    def retrieve_blogs(self, name): # stroy 5

        if self.current_user is None: # checking if already logged in
            raise IllegalAccessException()
        
        return self.blog_dao.retrieve_blogs(name)  # Delegate to DAO
    
    def update_blog(self, old_id, new_id, name, url, email):
        if self.current_user is None:
            raise IllegalAccessException()
        
        # Check if trying to update current blog
        if self.current_blog and self.current_blog.blog_id == old_id:
            raise IllegalOperationException()
        
        # Find the blog to update using DAO
        blog_to_update = self.blog_dao.search_blog(old_id)
        if blog_to_update is None:
            raise IllegalOperationException()
        
        # Check if new_id conflicts with existing blogs
        if old_id != new_id:
            if self.blog_dao.search_blog(new_id) is not None:
                raise IllegalOperationException()
        
        # Create updated blog object
        updated_blog = Blog(new_id, name, url, email)
        
        # Use DAO to perform the update - this should return the updated blog
        result = self.blog_dao.update_blog(old_id, updated_blog)
        
        if result is None:
            raise IllegalOperationException()
        
        return result  

    def delete_blog(self, blog_id):  # story 7
        if self.current_user is None:
            raise IllegalAccessException()
        
        if self.current_blog and self.current_blog.blog_id == blog_id:
            raise IllegalOperationException()
        
        success = self.blog_dao.delete_blog(blog_id)
        if not success:
            raise IllegalOperationException()

        if self.current_blog and self.current_blog.blog_id == blog_id:
            self.current_blog = None

        return True

        
    def list_blogs(self): #story 8

        if self.current_user is None:  # check if already logged in
            raise IllegalAccessException()
        
        return self.blog_dao.list_blogs()  # Delegate to DAO

    def set_current_blog(self, blog_id):
        if self.current_user is None:
            raise IllegalAccessException()
        # we used the two commented lines debigging becuase we had errors adn we didnt know where they were
        # print(f"DEBUG set_current_blog: Searching for blog {blog_id}")
        blog = self.search_blog(blog_id)
        # print(f"DEBUG set_current_blog: Found blog: {blog}")
        
        if blog is not None:
            self.current_blog = blog
            return True
        raise IllegalOperationException()

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
    def create_post(self, title: str, text: str): # story 10
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
        # Delegate to current blog's create_post method
        return blog.create_post(title, text) # The newly created post, or None if requirements not met
    
    def search_post(self, post_id: int):
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
        return blog.search_post(post_id) # The found post, or None if not found or requirements not met


    def retrieve_posts(self, query: str): # story 11
        # Check 1: Is user logged in?
        if self.current_user is None:
            raise IllegalAccessException()
        # Check 2: Is there a current blog selected?
        if self.current_blog is None:
            raise NoCurrentBlogException()
        blog = self.get_current_blog()
        if blog is None:
          return None
        return blog.retrieve_posts(query) # Matching posts sorted by ID, or None if requirements not met
    

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
        return blog.update_post(post_id, title, text) # True if post was updated, False otherwise

    def delete_post(self, post_id: int): # story 13
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
        return blog.delete_post(post_id) # True if post was deleted, False otherwise

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
        return blog.list_posts() # All posts sorted by ID descending, or None if requirements not met