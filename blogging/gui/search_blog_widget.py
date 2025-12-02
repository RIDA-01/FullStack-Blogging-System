
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from blogging.exception.illegal_access_exception import IllegalAccessException


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
