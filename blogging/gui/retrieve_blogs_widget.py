from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView
from blogging.exception.illegal_access_exception import IllegalAccessException
from .blog_table_model import BlogTableModel 

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
