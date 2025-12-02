from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QMessageBox
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from .blog_table_model import BlogTableModel 


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
            