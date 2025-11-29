
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

