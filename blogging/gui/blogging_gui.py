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

class BlogTableModel(QAbstractTableModel):
    def __init__(self, blogs=None):
        super().__init__()
        self.blogs = blogs or []
        self.headers = ['ID', 'Name', 'URL', 'Email']

    def rowCount(self, parent=None):
        return len(self.blogs)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        blog = self.blogs[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return str(blog.blog_id)
            elif index.column() == 1:
                return blog.name
            elif index.column() == 2:
                return blog.url
            elif index.column() == 3:
                return blog.email
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def update_data(self, blogs):
        self.beginResetModel()
        self.blogs = blogs
        self.endResetModel()

class LoginWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Blogging System - Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.status_label.setText("Please enter both username and password")
            return
            
        try:
            success = self.main_window.controller.login(username, password)
            if success:
                self.main_window.show_main_menu()
                self.status_label.setText("")
        except InvalidLoginException:
            self.status_label.setText("Invalid username or password")
        except DuplicateLoginException:
            self.status_label.setText("Already logged in")

class MainMenuWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Welcome message
        welcome = QLabel(f"Welcome to Blogging System")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 16px; margin: 20px;")
        layout.addWidget(welcome)
        
        # Blog Management Section
        blog_section = QLabel("Blog Management")
        blog_section.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(blog_section)
        
        # Blog buttons
        create_blog_btn = QPushButton("Create New Blog")
        create_blog_btn.clicked.connect(self.main_window.show_create_blog)
        layout.addWidget(create_blog_btn)
        
        search_blog_btn = QPushButton("Search Blog by ID")
        search_blog_btn.clicked.connect(self.main_window.show_search_blog)
        layout.addWidget(search_blog_btn)
        
        retrieve_blogs_btn = QPushButton("Retrieve Blogs by Name")
        retrieve_blogs_btn.clicked.connect(self.main_window.show_retrieve_blogs)
        layout.addWidget(retrieve_blogs_btn)
        
        list_blogs_btn = QPushButton("List All Blogs")
        list_blogs_btn.clicked.connect(self.main_window.show_list_blogs)
        layout.addWidget(list_blogs_btn)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        self.setLayout(layout)

    def logout(self):
        try:
            self.main_window.controller.logout()
            self.main_window.show_login()
        except Exception as e:
            QMessageBox.warning(self, "Logout Error", str(e))

class SearchBlogWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Search Blog by ID")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Blog ID input
        layout.addWidget(QLabel("Blog ID:"))
        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("Enter blog ID number")
        layout.addWidget(self.blog_id_input)
        
        # Search button
        search_btn = QPushButton("Search Blog")
        search_btn.clicked.connect(self.search_blog)
        layout.addWidget(search_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        layout.addWidget(back_btn)
        
        # Results area
        self.results_label = QLabel("")
        self.results_label.setStyleSheet("margin: 20px;")
        layout.addWidget(self.results_label)
        
        self.setLayout(layout)

    def search_blog(self):
        blog_id_text = self.blog_id_input.text().strip()
        
        if not blog_id_text:
            self.results_label.setText("Please enter a blog ID")
            self.results_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        try:
            blog_id = int(blog_id_text)
            blog = self.main_window.controller.search_blog(blog_id)
            
            if blog:
                result_text = f"""
                <h3>Blog Found:</h3>
                <b>ID:</b> {blog.blog_id}<br>
                <b>Name:</b> {blog.name}<br>
                <b>URL:</b> {blog.url}<br>
                <b>Email:</b> {blog.email}
                """
                self.results_label.setText(result_text)
                self.results_label.setStyleSheet("color: green; margin: 20px;")
            else:
                self.results_label.setText(f"No blog found with ID: {blog_id}")
                self.results_label.setStyleSheet("color: red; margin: 20px;")
                
        except ValueError:
            self.results_label.setText("Please enter a valid number for Blog ID")
            self.results_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalAccessException:
            self.results_label.setText("Error: You must be logged in to search blogs")
            self.results_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.results_label.setText(f"Error searching blog: {str(e)}")
            self.results_label.setStyleSheet("color: red; margin: 20px;")

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
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.search_blog_widget)
        
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
        """Show create blog screen - to be implemented"""
        QMessageBox.information(self, "Info", "Create Blog feature - To be implemented")
        
    def show_retrieve_blogs(self):
        """Show retrieve blogs screen - to be implemented"""
        QMessageBox.information(self, "Info", "Retrieve Blogs feature - To be implemented")
        
    def show_list_blogs(self):
        """Show list all blogs screen - to be implemented"""
        QMessageBox.information(self, "Info", "List All Blogs feature - To be implemented")

def main():
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()