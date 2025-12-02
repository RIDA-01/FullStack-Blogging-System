from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt



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
