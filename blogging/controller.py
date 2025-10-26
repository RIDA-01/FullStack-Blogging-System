class Controller:
    def __init__(self):
        self.current_user = None
        # Hardcoded user for now - from the test
        self.users = {"user": "blogging2025"}
    
    def login(self, username, password):    
        if self.current_user is not None:#checking if already logged in
            return False
            
        if username in self.users and self.users[username] == password: #checking username exists and password matche
            self.current_user = username
            return True
        return False
    
    def logout(self):
        if self.current_user is not None:#if logged in then u can log out
            self.current_user = None
            return True
        return False