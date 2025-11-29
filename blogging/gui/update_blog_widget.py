
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
