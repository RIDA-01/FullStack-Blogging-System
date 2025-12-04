from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class UpdatePostWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_post = None   # store loaded post
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Update Post")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Post code input
        layout.addWidget(QLabel("Post number (ID):"))
        self.post_code_input = QLineEdit()
        self.post_code_input.setPlaceholderText("Enter post number, e.g. 1")
        layout.addWidget(self.post_code_input)

        # Load + Back buttons
        top_buttons = QHBoxLayout()

        load_btn = QPushButton("Load Post")
        load_btn.clicked.connect(self.load_post)
        top_buttons.addWidget(load_btn)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        top_buttons.addWidget(back_btn)

        layout.addLayout(top_buttons)

        # Editable title/text
        layout.addWidget(QLabel("New Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("New Text:"))
        self.text_input = QPlainTextEdit()
        layout.addWidget(self.text_input)

        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        layout.addWidget(save_btn)

        # Status label
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
                self.title_input.clear()
                self.text_input.clear()
                self.status_label.setText("No post found with this number.")
                self.status_label.setStyleSheet("color: red; margin: 10px;")
                return

            # Fill fields with existing data
            self.current_post = post
            self.title_input.setText(post.title)
            self.text_input.setPlainText(post.text)
            self.status_label.setText(f"Loaded post #{post.code}.")
            self.status_label.setStyleSheet("color: green; margin: 10px;")

        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to update posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error loading post: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")

    def save_changes(self):
        if self.current_post is None:
            self.status_label.setText("Load a post first before saving.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return

        new_title = self.title_input.text().strip()
        new_text = self.text_input.toPlainText().strip()

        if not new_title or not new_text:
            self.status_label.setText("Title and text cannot be empty.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            return

        try:
            controller = self.main_window.controller
            controller.update_post(self.current_post.code, new_title, new_text)

            self.status_label.setText("Post updated successfully.")
            self.status_label.setStyleSheet("color: green; margin: 10px;")

        except IllegalAccessException:
            self.status_label.setText("Error: You must be logged in to update posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.status_label.setText(f"Error updating post: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
