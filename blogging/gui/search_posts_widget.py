from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class SearchPostsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Search Posts by Text")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Search input
        layout.addWidget(QLabel("Search for:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search in posts")
        layout.addWidget(self.search_input)

        # Buttons row
        buttons_layout = QHBoxLayout()

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_posts)
        buttons_layout.addWidget(search_btn)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)

        layout.addLayout(buttons_layout)

        # Results area
        self.results_area = QPlainTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def search_posts(self):
        text = self.search_input.text().strip()

        if not text:
            self.status_label.setText("Please enter some text to search.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
            self.results_area.setPlainText("")
            return

        try:
            controller = self.main_window.controller
            # same method as CLI: controller.retrieve_posts(search_string)
            posts = controller.retrieve_posts(text)

            if not posts:
                self.results_area.setPlainText(f"No posts found for: {text}")
                self.status_label.setText("")
                return

            lines = []
            for post in posts:
                lines.append(
                    f"Post #{post.code}, created - {post.creation_time}, changed - {post.update_time}\n"
                    f"Title: {post.title}\n"
                    f"{post.text}\n"
                    + "-" * 40
                )

            self.results_area.setPlainText("\n\n".join(lines))
            self.status_label.setText("Posts found.")
            self.status_label.setStyleSheet("color: green; margin: 10px;")

        except IllegalAccessException:
            self.results_area.setPlainText("")
            self.status_label.setText("Error: You must be logged in to search posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.results_area.setPlainText("")
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.results_area.setPlainText("")
            self.status_label.setText(f"Error searching posts: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
