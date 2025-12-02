import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, 
                             QVBoxLayout, QWidget, QMessageBox, QTableView,
                             QPlainTextEdit, QHeaderView, QLabel, 
                             QLineEdit, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, QAbstractTableModel
from blogging.configuration import Configuration
from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from .login_widget import LoginWidget
from .main_menu_widget import MainMenuWidget
from .search_blog_widget import SearchBlogWidget
from .create_blog_widget import CreateBlogWidget
from .retrieve_blogs_widget import RetrieveBlogsWidget
from .update_blog_widget import UpdateBlogWidget
from .delete_blog_widget import DeleteBlogWidget
from .list_blogs_widget import ListBlogsWidget
from .choose_current_blog_widget import ChooseCurrentBlogWidget
            


class BloggingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        self.controller = Controller()
        
        # Start with smaller login window
        self.setWindowTitle("Blogging System - Login")
        self.setGeometry(100, 100, 400, 300)  # Smaller size for login
        
        self.setup_ui()
        self.show_login()
        
    def setup_ui(self):
        """Setup the main UI components"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Create different screens
        self.login_widget = LoginWidget(self)
        self.main_menu_widget = MainMenuWidget(self)
        self.search_blog_widget = SearchBlogWidget(self)
        self.create_blog_widget = CreateBlogWidget(self)
        self.retrieve_blogs_widget = RetrieveBlogsWidget(self) 
        self.update_blog_widget = UpdateBlogWidget(self)
        self.delete_blog_widget = DeleteBlogWidget(self)
        self.list_blogs_widget = ListBlogsWidget(self)
        self.choose_current_blog_widget = ChooseCurrentBlogWidget(self)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.search_blog_widget)
        self.stacked_widget.addWidget(self.create_blog_widget)
        self.stacked_widget.addWidget(self.retrieve_blogs_widget)
        self.stacked_widget.addWidget(self.update_blog_widget) 
        self.stacked_widget.addWidget(self.delete_blog_widget)
        self.stacked_widget.addWidget(self.list_blogs_widget)
        self.stacked_widget.addWidget(self.choose_current_blog_widget) 
        
    def show_login(self):
        """Show login screen - smaller window"""
        self.stacked_widget.setCurrentWidget(self.login_widget)
        self.setWindowTitle("Blogging System - Login")
        self.resize(400, 300)  # Small size for login
        
    def show_main_menu(self):
        """Show main menu - larger window"""
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        self.setWindowTitle("Blogging System - Main Menu")
        self.resize(600, 400)  # Larger size for main menu
        
    def show_search_blog(self):
        """Show search blog screen"""
        self.stacked_widget.setCurrentWidget(self.search_blog_widget)
        self.setWindowTitle("Blogging System - Search Blog")
        self.resize(500, 400)  # Medium size for search
        
    def show_create_blog(self):
            """Show create blog screen"""
            self.stacked_widget.setCurrentWidget(self.create_blog_widget)
            self.setWindowTitle("Blogging System - Create Blog")
            self.resize(500, 500)  # Good size for form inputs
        
    def show_retrieve_blogs(self):
        """Show retrieve blogs by name screen"""
        self.stacked_widget.setCurrentWidget(self.retrieve_blogs_widget)
        self.setWindowTitle("Blogging System - Retrieve Blogs by Name")
        self.resize(700, 500)

    def show_update_blog(self):
        """Show update blog screen"""
        self.stacked_widget.setCurrentWidget(self.update_blog_widget)
        self.setWindowTitle("Blogging System - Update Blog")
        self.resize(500, 500)
    
    def show_delete_blog(self):
        """Show delete blog screen"""
        self.stacked_widget.setCurrentWidget(self.delete_blog_widget)
        self.setWindowTitle("Blogging System - Delete Blog")
        self.resize(500, 400)
        
    def show_list_blogs(self):
        """Show list all blogs screen"""
        self.stacked_widget.setCurrentWidget(self.list_blogs_widget)
        self.setWindowTitle("Blogging System - List All Blogs")
        self.resize(700, 500)  
        # Auto-load blogs when showing this screen
        self.list_blogs_widget.load_blogs()

    def show_choose_current_blog(self):
        """Show choose current blog screen"""
        self.stacked_widget.setCurrentWidget(self.choose_current_blog_widget)
        self.setWindowTitle("Blogging System - Choose Current Blog")
        self.resize(700, 500)  
        # Auto-load blogs when showing this screen
        self.choose_current_blog_widget.load_blogs()   

def main():
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()