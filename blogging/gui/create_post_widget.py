from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class CreatePostWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Create New Post")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Post title
        layout.addWidget(QLabel("Post Title:"))
        self.post_title_input = QLineEdit()
        self.post_title_input.setPlaceholderText("Enter Post Title")
        layout.addWidget(self.post_title_input)

        # Post content
        layout.addWidget(QLabel("Post Text:"))
        self.post_text_input = QPlainTextEdit()
        self.post_text_input.setPlaceholderText("Enter post content")
        layout.addWidget(self.post_text_input)

        # Buttons
        buttons_layout = QHBoxLayout()

        # Create button
        create_btn = QPushButton("Create Post")
        create_btn.clicked.connect(self.create_post)
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
        """Clear all input fields (keep status message)."""
        self.post_title_input.clear()
        self.post_text_input.clear()
        # Do not clear status_label here so success/error messages stay visible

    def create_post(self):
        """Create a new post with the provided data."""
        title = self.post_title_input.text().strip()
        text = self.post_text_input.toPlainText().strip()

        # Validate inputs
        if not title:
            self.status_label.setText("Please enter a Post Title")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return

        if not text:
            self.status_label.setText("Please enter Post Text")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
            return

        try:
            # Use controller to create the post
            self.main_window.controller.create_post(title, text)

            # Show success message
            self.status_label.setText("Post created successfully.")
            self.status_label.setStyleSheet("color: green; margin: 20px;")

            # Clear inputs but keep the success message
            self.clear_form()

        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to create posts")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except NoCurrentBlogException:
            self.status_label.setText("Error: You must select a current blog before creating posts")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
        except Exception as e:
            self.status_label.setText(f"Error creating post: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 20px;")
