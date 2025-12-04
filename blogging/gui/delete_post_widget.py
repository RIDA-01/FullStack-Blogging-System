from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class DeletePostWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_post = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Delete Post")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Post number
        layout.addWidget(QLabel("Post number (ID):"))
        self.post_code_input = QLineEdit()
        self.post_code_input.setPlaceholderText("Enter post number, e.g. 1")
        layout.addWidget(self.post_code_input)

        # Buttons row
        buttons_layout = QHBoxLayout()

        load_btn = QPushButton("Load Post")
        load_btn.clicked.connect(self.load_post)
        buttons_layout.addWidget(load_btn)

        delete_btn = QPushButton("Delete Post")
        delete_btn.clicked.connect(self.delete_post)
        buttons_layout.addWidget(delete_btn)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)

        layout.addLayout(buttons_layout)

        # Show post details (read-only)
        self.post_preview = QPlainTextEdit()
        self.post_preview.setReadOnly(True)
        layout.addWidget(self.post_preview)

        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_post(self):
        code_text = self.post_code_input.text().strip()

        if not code_text:
            self.status_label.setText("Please enter a post number.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return

        try:
            code = int(code_text)
        except ValueError:
            self.status_label.setText("Post number must be an integer.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return

        try:
            controller = self.main_window.controller
            post = controller.search_post(code)

            if post is None:
                self.current_post = None
                self.post_preview.setPlainText("")
                self.status_label.setText("No post found with this number.")
                self.status_label.setStyleSheet("color: red; margin: 10px;")
                return

            self.current_post = post
            preview_text = (
                f"Post #{post.code}\n"
                f"Created: {post.creation_time}\n"
                f"Updated: {post.update_time}\n\n"
                f"Title: {post.title}\n\n"
                f"{post.text}"
            )
            self.post_preview.setPlainText(preview_text)
            self.status_label.setText("Post loaded. Click 'Delete Post' to remove it.")
            self.status_label.setStyleSheet("color: orange; margin: 10px;")

        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to load posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error loading post: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")

    def delete_post(self):
        if self.current_post is None:
            self.status_label.setText("Load a post first before deleting.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return

        try:
            controller = self.main_window.controller
            controller.delete_post(self.current_post.code)

            self.post_preview.setPlainText("")
            self.post_code_input.clear()
            self.current_post = None

            self.status_label.setText("Post deleted successfully.")
            self.status_label.setStyleSheet("color: green; margin: 10px;")

        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to delete posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error deleting post: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
