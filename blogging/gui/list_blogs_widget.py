from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from blogging.exception.illegal_access_exception import IllegalAccessException
from .blog_table_model import BlogTableModel

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
