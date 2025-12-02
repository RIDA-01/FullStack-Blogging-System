
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