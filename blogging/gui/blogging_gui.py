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

        update_blog_btn = QPushButton("Update Existing Blog")
        update_blog_btn.clicked.connect(self.main_window.show_update_blog)
        layout.addWidget(update_blog_btn)
        
        search_blog_btn = QPushButton("Search Blog by ID")
        search_blog_btn.clicked.connect(self.main_window.show_search_blog)
        layout.addWidget(search_blog_btn)
        
        retrieve_blogs_btn = QPushButton("Retrieve Blogs by Name")
        retrieve_blogs_btn.clicked.connect(self.main_window.show_retrieve_blogs)
        layout.addWidget(retrieve_blogs_btn)

        delete_blog_btn = QPushButton("Delete Existing Blog")
        delete_blog_btn.clicked.connect(self.main_window.show_delete_blog)
        layout.addWidget(delete_blog_btn)
        
        list_blogs_btn = QPushButton("List All Blogs")
        list_blogs_btn.clicked.connect(self.main_window.show_list_blogs)  
        layout.addWidget(list_blogs_btn)

        # Post Management Section
        post_section = QLabel("Post Management")
        post_section.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(post_section)

        choose_blog_btn = QPushButton("Choose Current Blog for Editing")
        choose_blog_btn.clicked.connect(self.main_window.show_choose_current_blog)
        layout.addWidget(choose_blog_btn)
        
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

class CreateBlogWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Create New Blog")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Blog ID input
        layout.addWidget(QLabel("Blog ID:"))
        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("Enter unique blog ID number")
        layout.addWidget(self.blog_id_input)
        
        # Blog Name input
        layout.addWidget(QLabel("Blog Name:"))
        self.blog_name_input = QLineEdit()
        self.blog_name_input.setPlaceholderText("Enter blog name")
        layout.addWidget(self.blog_name_input)
        
        # Blog URL input
        layout.addWidget(QLabel("Blog URL:"))
        self.blog_url_input = QLineEdit()
        self.blog_url_input.setPlaceholderText("Enter blog URL")
        layout.addWidget(self.blog_url_input)
        
        # Blog Email input
        layout.addWidget(QLabel("Blog Email:"))
        self.blog_email_input = QLineEdit()
        self.blog_email_input.setPlaceholderText("Enter blog email")
        layout.addWidget(self.blog_email_input)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Create button
        create_btn = QPushButton("Create Blog")
        create_btn.clicked.connect(self.create_blog)
        buttons_layout.addWidget(create_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(clear_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 20px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def clear_form(self):
        """Clear all input fields"""
        self.blog_id_input.clear()
        self.blog_name_input.clear()
        self.blog_url_input.clear()
        self.blog_email_input.clear()
        self.status_label.setText("")

    def create_blog(self):
        """Create a new blog with the provided data"""
        blog_id_text = self.blog_id_input.text().strip()
        blog_name = self.blog_name_input.text().strip()
        blog_url = self.blog_url_input.text().strip()
        blog_email = self.blog_email_input.text().strip()
        
        # Validate inputs
        if not blog_id_text:
            self.status_label.setText("Please enter a Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        if not blog_name:
            self.status_label.setText("Please enter a Blog Name")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        if not blog_url:
            self.status_label.setText("Please enter a Blog URL")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        if not blog_email:
            self.status_label.setText("Please enter a Blog Email")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        try:
            blog_id = int(blog_id_text)
            
            # Call controller to create blog
            created_blog = self.main_window.controller.create_blog(blog_id, blog_name, blog_url, blog_email)
            
            if created_blog:
                success_text = f"""
                <h3>Blog Created Successfully!</h3>
                <b>ID:</b> {created_blog.blog_id}<br>
                <b>Name:</b> {created_blog.name}<br>
                <b>URL:</b> {created_blog.url}<br>
                <b>Email:</b> {created_blog.email}
                """
                self.status_label.setText(success_text)
                self.status_label.setStyleSheet("color: green; margin: 20px;")
                
                # Clear form for next entry
                self.clear_form()
                
        except ValueError:
            self.status_label.setText("Please enter a valid number for Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to create blogs")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalOperationException:
            self.status_label.setText("Error: A blog with this ID already exists")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.status_label.setText(f"Error creating blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")

class RetrieveBlogsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Retrieve Blogs by Name")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Search input
        layout.addWidget(QLabel("Search Blog Name:"))
        self.search_name_input = QLineEdit()
        self.search_name_input.setPlaceholderText("Enter blog name or part of name to search")
        layout.addWidget(self.search_name_input)
        
        # Search button
        search_btn = QPushButton("Search Blogs")
        search_btn.clicked.connect(self.search_blogs)
        layout.addWidget(search_btn)
        
        # Results table (REQUIRED by assignment - QTableView)
        self.results_label = QLabel("Enter a search term and click 'Search Blogs'")
        self.results_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.results_label)
        
        self.blog_table = QTableView()
        self.blog_model = BlogTableModel()
        self.blog_table.setModel(self.blog_model)
        
        # Set table properties
        self.blog_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.blog_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.blog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.blog_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.blog_table)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Clear button
        clear_btn = QPushButton("Clear Search")
        clear_btn.clicked.connect(self.clear_search)
        buttons_layout.addWidget(clear_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def clear_search(self):
        """Clear search results"""
        self.search_name_input.clear()
        self.blog_model.update_data([])
        self.results_label.setText("Enter a search term and click 'Search Blogs'")
        self.results_label.setStyleSheet("margin: 10px;")

    def search_blogs(self):
        """Search blogs by name"""
        search_term = self.search_name_input.text().strip()
        
        if not search_term:
            self.results_label.setText("Please enter a search term")
            self.results_label.setStyleSheet("color: red; margin: 10px;")
            return
            
        try:
            blogs = self.main_window.controller.retrieve_blogs(search_term)
            
            if blogs:
                self.blog_model.update_data(blogs)
                self.results_label.setText(f"Found {len(blogs)} blog(s) matching '{search_term}'")
                self.results_label.setStyleSheet("color: green; margin: 10px;")
            else:
                self.blog_model.update_data([])
                self.results_label.setText(f"No blogs found matching '{search_term}'")
                self.results_label.setStyleSheet("color: orange; margin: 10px;")
                
        except IllegalAccessException:
            self.results_label.setText("Error: You must be logged in to search blogs")
            self.results_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.results_label.setText(f"Error searching blogs: {str(e)}")
            self.results_label.setStyleSheet("color: red; margin: 10px;")

class UpdateBlogWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_blog = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Update Existing Blog")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Blog ID search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Enter Blog ID to update:"))
        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("Enter blog ID number")
        search_layout.addWidget(self.blog_id_input)
        
        self.load_blog_btn = QPushButton("Load Blog")
        self.load_blog_btn.clicked.connect(self.load_blog)
        search_layout.addWidget(self.load_blog_btn)
        
        layout.addLayout(search_layout)
        
        # Blog details form (initially disabled)
        form_layout = QVBoxLayout()
        
        # Blog ID (display only)
        form_layout.addWidget(QLabel("Blog ID (cannot change):"))
        self.blog_id_display = QLineEdit()
        self.blog_id_display.setEnabled(False)
        form_layout.addWidget(self.blog_id_display)
        
        # Blog Name
        form_layout.addWidget(QLabel("Blog Name:"))
        self.blog_name_input = QLineEdit()
        self.blog_name_input.setPlaceholderText("Enter new blog name")
        form_layout.addWidget(self.blog_name_input)
        
        # Blog URL
        form_layout.addWidget(QLabel("Blog URL:"))
        self.blog_url_input = QLineEdit()
        self.blog_url_input.setPlaceholderText("Enter new blog URL")
        form_layout.addWidget(self.blog_url_input)
        
        # Blog Email
        form_layout.addWidget(QLabel("Blog Email:"))
        self.blog_email_input = QLineEdit()
        self.blog_email_input.setPlaceholderText("Enter new blog email")
        form_layout.addWidget(self.blog_email_input)
        
        layout.addLayout(form_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Update button (initially disabled)
        self.update_btn = QPushButton("Update Blog")
        self.update_btn.clicked.connect(self.update_blog)
        self.update_btn.setEnabled(False)
        buttons_layout.addWidget(self.update_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(clear_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Enter a Blog ID and click 'Load Blog' to start")
        self.status_label.setStyleSheet("margin: 20px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Initially disable the form
        self.set_form_enabled(False)

    def set_form_enabled(self, enabled):
        """Enable or disable the form fields"""
        self.blog_name_input.setEnabled(enabled)
        self.blog_url_input.setEnabled(enabled)
        self.blog_email_input.setEnabled(enabled)
        self.update_btn.setEnabled(enabled)

    def clear_form(self):
        """Clear all input fields"""
        self.blog_id_input.clear()
        self.blog_id_display.clear()
        self.blog_name_input.clear()
        self.blog_url_input.clear()
        self.blog_email_input.clear()
        self.status_label.setText("Enter a Blog ID and click 'Load Blog' to start")
        self.status_label.setStyleSheet("margin: 20px;")
        self.set_form_enabled(False)
        self.current_blog = None

    def load_blog(self):
        """Load a blog for editing"""
        blog_id_text = self.blog_id_input.text().strip()
        
        if not blog_id_text:
            self.status_label.setText("Please enter a Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        try:
            blog_id = int(blog_id_text)
            blog = self.main_window.controller.search_blog(blog_id)
            
            if blog:
                # Check if trying to update current blog
                current_blog = self.main_window.controller.get_current_blog()
                if current_blog and current_blog.blog_id == blog_id:
                    self.status_label.setText("Error: Cannot update the current blog. Finish editing it first.")
                    self.status_label.setStyleSheet("color: red; margin: 20px;")
                    return
                
                # Populate form with blog data
                self.current_blog = blog
                self.blog_id_display.setText(str(blog.blog_id))
                self.blog_name_input.setText(blog.name)
                self.blog_url_input.setText(blog.url)
                self.blog_email_input.setText(blog.email)
                
                self.set_form_enabled(True)
                self.status_label.setText("Blog loaded. Make changes and click 'Update Blog'")
                self.status_label.setStyleSheet("color: green; margin: 20px;")
                
            else:
                self.status_label.setText(f"No blog found with ID: {blog_id}")
                self.status_label.setStyleSheet("color: red; margin: 20px;")
                self.set_form_enabled(False)
                
        except ValueError:
            self.status_label.setText("Please enter a valid number for Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to update blogs")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.status_label.setText(f"Error loading blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")

    def update_blog(self):
        """Update the blog with new data"""
        if not self.current_blog:
            self.status_label.setText("Error: No blog loaded for updating")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        blog_name = self.blog_name_input.text().strip()
        blog_url = self.blog_url_input.text().strip()
        blog_email = self.blog_email_input.text().strip()
        
        # Validate inputs
        if not blog_name:
            self.status_label.setText("Please enter a Blog Name")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        if not blog_url:
            self.status_label.setText("Please enter a Blog URL")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        if not blog_email:
            self.status_label.setText("Please enter a Blog Email")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        try:
            old_id = self.current_blog.blog_id
            
            # Call controller to update blog (using same ID)
            updated_blog = self.main_window.controller.update_blog(
                old_id, old_id, blog_name, blog_url, blog_email
            )
            
            if updated_blog:
                success_text = f"""
                <h3>Blog Updated Successfully!</h3>
                <b>ID:</b> {updated_blog.blog_id}<br>
                <b>Name:</b> {updated_blog.name}<br>
                <b>URL:</b> {updated_blog.url}<br>
                <b>Email:</b> {updated_blog.email}
                """
                self.status_label.setText(success_text)
                self.status_label.setStyleSheet("color: green; margin: 20px;")
                
                # Keep form enabled for further edits
                self.current_blog = updated_blog
                
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to update blogs")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalOperationException as e:
            self.status_label.setText(f"Error updating blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.status_label.setText(f"Error updating blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")

class DeleteBlogWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_blog = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Delete Existing Blog")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Blog ID search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Enter Blog ID to delete:"))
        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("Enter blog ID number")
        search_layout.addWidget(self.blog_id_input)
        
        self.load_blog_btn = QPushButton("Load Blog")
        self.load_blog_btn.clicked.connect(self.load_blog)
        search_layout.addWidget(self.load_blog_btn)
        
        layout.addLayout(search_layout)
        
        # Blog details display (read-only)
        details_layout = QVBoxLayout()
        
        details_layout.addWidget(QLabel("Blog Details:"))
        self.blog_details_display = QLabel("No blog loaded")
        self.blog_details_display.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        self.blog_details_display.setWordWrap(True)
        details_layout.addWidget(self.blog_details_display)
        
        layout.addLayout(details_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Delete button (initially disabled)
        self.delete_btn = QPushButton("Delete Blog")
        self.delete_btn.clicked.connect(self.delete_blog)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold;")
        buttons_layout.addWidget(self.delete_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        buttons_layout.addWidget(clear_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Enter a Blog ID and click 'Load Blog' to start")
        self.status_label.setStyleSheet("margin: 20px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def clear_form(self):
        """Clear all input fields"""
        self.blog_id_input.clear()
        self.blog_details_display.setText("No blog loaded")
        self.status_label.setText("Enter a Blog ID and click 'Load Blog' to start")
        self.status_label.setStyleSheet("margin: 20px;")
        self.delete_btn.setEnabled(False)
        self.current_blog = None

    def load_blog(self):
        """Load a blog for deletion confirmation"""
        blog_id_text = self.blog_id_input.text().strip()
        
        if not blog_id_text:
            self.status_label.setText("Please enter a Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        try:
            blog_id = int(blog_id_text)
            blog = self.main_window.controller.search_blog(blog_id)
            
            if blog:
                # Check if trying to delete current blog
                current_blog = self.main_window.controller.get_current_blog()
                if current_blog and current_blog.blog_id == blog_id:
                    self.status_label.setText("Error: Cannot delete the current blog. Finish editing it first.")
                    self.status_label.setStyleSheet("color: red; margin: 20px;")
                    self.blog_details_display.setText("No blog loaded")
                    self.delete_btn.setEnabled(False)
                    return
                
                # Display blog details
                self.current_blog = blog
                details_text = f"""
                <b>ID:</b> {blog.blog_id}<br>
                <b>Name:</b> {blog.name}<br>
                <b>URL:</b> {blog.url}<br>
                <b>Email:</b> {blog.email}
                """
                self.blog_details_display.setText(details_text)
                
                self.delete_btn.setEnabled(True)
                self.status_label.setText("Blog loaded. Review details and click 'Delete Blog' to confirm")
                self.status_label.setStyleSheet("color: orange; margin: 20px;")
                
            else:
                self.status_label.setText(f"No blog found with ID: {blog_id}")
                self.status_label.setStyleSheet("color: red; margin: 20px;")
                self.blog_details_display.setText("No blog loaded")
                self.delete_btn.setEnabled(False)
                
        except ValueError:
            self.status_label.setText("Please enter a valid number for Blog ID")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to delete blogs")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.status_label.setText(f"Error loading blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")

    def delete_blog(self):
        """Delete the loaded blog after confirmation"""
        if not self.current_blog:
            self.status_label.setText("Error: No blog loaded for deletion")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return
            
        # Confirmation dialog
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion",
            f"Are you sure you want to delete blog '{self.current_blog.name}' (ID: {self.current_blog.blog_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                blog_id = self.current_blog.blog_id
                success = self.main_window.controller.delete_blog(blog_id)
                
                if success:
                    success_text = f"Blog '{self.current_blog.name}' (ID: {blog_id}) deleted successfully!"
                    self.status_label.setText(success_text)
                    self.status_label.setStyleSheet("color: green; margin: 20px;")
                    
                    # Clear form after successful deletion
                    self.blog_details_display.setText("No blog loaded")
                    self.delete_btn.setEnabled(False)
                    self.current_blog = None
                    
            except IllegalAccessException:
                self.status_label.setText("Error: You must be logged in to delete blogs")
                self.status_label.setStyleSheet("color: red; margin: 20px;")
            except IllegalOperationException as e:
                self.status_label.setText(f"Error deleting blog: {str(e)}")
                self.status_label.setStyleSheet("color: red; margin: 20px;")
            except Exception as e:
                self.status_label.setText(f"Error deleting blog: {str(e)}")
                self.status_label.setStyleSheet("color: red; margin: 20px;")
class ListBlogsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("List All Blogs")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Status label
        self.status_label = QLabel("Click 'Refresh' to load all blogs")
        self.status_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.status_label)
        
        # Table view for blogs (REQUIRED by assignment - QTableView)
        self.blog_table = QTableView()
        self.blog_model = BlogTableModel()
        self.blog_table.setModel(self.blog_model)
        
        # Set table properties
        self.blog_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.blog_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.blog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.blog_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.blog_table)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self.load_blogs)
        buttons_layout.addWidget(refresh_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def load_blogs(self):
        """Load all blogs into the table view"""
        try:
            blogs = self.main_window.controller.list_blogs()
            
            if blogs:
                self.blog_model.update_data(blogs)
                self.status_label.setText(f"Loaded {len(blogs)} blog(s)")
                self.status_label.setStyleSheet("color: green; margin: 10px;")
            else:
                self.blog_model.update_data([])
                self.status_label.setText("No blogs found in the system")
                self.status_label.setStyleSheet("color: orange; margin: 10px;")
                
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to list blogs")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error loading blogs: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")

class ChooseCurrentBlogWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        # Don't call update_current_blog_status() here - wait until widget is shown

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Choose Current Blog for Editing")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Current blog status
        self.current_blog_label = QLabel("No blog currently selected for editing")
        self.current_blog_label.setStyleSheet("background-color: #fff3cd; padding: 10px; border: 1px solid #ffeaa7; margin: 10px;")
        layout.addWidget(self.current_blog_label)
        
        # Blog selection section
        selection_layout = QVBoxLayout()
        
        selection_layout.addWidget(QLabel("Select Blog to Edit:"))
        
        # Blog table view
        self.blog_table = QTableView()
        self.blog_model = BlogTableModel()
        self.blog_table.setModel(self.blog_model)
        
        # Set table properties
        self.blog_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.blog_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.blog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.blog_table.setAlternatingRowColors(True)
        
        selection_layout.addWidget(self.blog_table)
        
        # Selection buttons
        selection_buttons_layout = QHBoxLayout()
        
        self.select_blog_btn = QPushButton("Select Blog for Editing")
        self.select_blog_btn.clicked.connect(self.select_current_blog)
        selection_buttons_layout.addWidget(self.select_blog_btn)
        
        self.unselect_blog_btn = QPushButton("Stop Editing Current Blog")
        self.unselect_blog_btn.clicked.connect(self.unselect_current_blog)
        selection_buttons_layout.addWidget(self.unselect_blog_btn)
        
        selection_layout.addLayout(selection_buttons_layout)
        
        layout.addLayout(selection_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Blog List")
        refresh_btn.clicked.connect(self.load_blogs)
        buttons_layout.addWidget(refresh_btn)
        
        # Back button
        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Click 'Refresh Blog List' to load available blogs")
        self.status_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Don't update current blog status here - it will be called when the widget is shown

    def showEvent(self, event):
        """Override showEvent to update status when widget becomes visible"""
        super().showEvent(event)
        self.update_current_blog_status()

    def update_current_blog_status(self):
        """Update the display of current blog status"""
        try:
            current_blog = self.main_window.controller.get_current_blog()
            if current_blog:
                status_text = f"""
                <b>Currently Editing:</b><br>
                <b>ID:</b> {current_blog.blog_id}<br>
                <b>Name:</b> {current_blog.name}<br>
                <b>URL:</b> {current_blog.url}
                """
                self.current_blog_label.setText(status_text)
                self.current_blog_label.setStyleSheet("background-color: #d4edda; padding: 10px; border: 1px solid #c3e6cb; margin: 10px;")
            else:
                self.current_blog_label.setText("No blog currently selected for editing")
                self.current_blog_label.setStyleSheet("background-color: #fff3cd; padding: 10px; border: 1px solid #ffeaa7; margin: 10px;")
        except IllegalAccessException:
            # User not logged in - this should not happen in normal flow
            self.current_blog_label.setText("Please log in first")
            self.current_blog_label.setStyleSheet("background-color: #f8d7da; padding: 10px; border: 1px solid #f5c6cb; margin: 10px;")

    def load_blogs(self):
        """Load all blogs into the table view"""
        try:
            blogs = self.main_window.controller.list_blogs()
            
            if blogs:
                self.blog_model.update_data(blogs)
                self.status_label.setText(f"Loaded {len(blogs)} blog(s). Select a blog to start editing.")
                self.status_label.setStyleSheet("color: green; margin: 10px;")
            else:
                self.blog_model.update_data([])
                self.status_label.setText("No blogs found in the system. Create a blog first.")
                self.status_label.setStyleSheet("color: orange; margin: 10px;")
                
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to list blogs")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error loading blogs: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")

    def select_current_blog(self):
        """Set the selected blog as current blog for editing"""
        selected_indexes = self.blog_table.selectionModel().selectedRows()
        
        if not selected_indexes:
            self.status_label.setText("Please select a blog from the list first")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return
            
        try:
            selected_row = selected_indexes[0].row()
            blog = self.blog_model.blogs[selected_row]
            blog_id = blog.blog_id
            
            # Set as current blog
            self.main_window.controller.set_current_blog(blog_id)
            
            # Update status
            self.update_current_blog_status()
            self.status_label.setText(f"Now editing blog: {blog.name} (ID: {blog_id})")
            self.status_label.setStyleSheet("color: green; margin: 10px;")
            
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to set current blog")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except IllegalOperationException:
            self.status_label.setText("Error: Blog not found or cannot be set as current")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error setting current blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")

    def unselect_current_blog(self):
        """Stop editing the current blog"""
        try:
            self.main_window.controller.unset_current_blog()
            
            # Update status
            self.update_current_blog_status()
            self.status_label.setText("Stopped editing current blog")
            self.status_label.setStyleSheet("color: green; margin: 10px;")
            
        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to unset current blog")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error unsetting current blog: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            
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