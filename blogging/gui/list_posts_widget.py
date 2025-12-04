from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPlainTextEdit,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class ListPostsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Blog Posts")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Text area for posts
        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        # Buttons
        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_posts)
        buttons_layout.addWidget(refresh_btn)

        back_btn = QPushButton("Back to Main Menu")
        back_btn.clicked.connect(self.main_window.show_main_menu)
        buttons_layout.addWidget(back_btn)

        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 10px;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_posts(self):
        """
        Retrieve all posts for current blog and show them in text_area.
        """
        try:
            controller = self.main_window.controller
            posts = controller.list_posts()

            if not posts:
                self.text_area.setPlainText("Blog is empty.")
                self.status_label.setText("")
                return

            lines = []
            for post in posts:
                # same as print_post_data in CLI
                lines.append(
                    f"Post #{post.code}, created - {post.creation_time}, changed - {post.update_time}\n"
                    f"Title: {post.title}\n"
                    f"{post.text}\n"
                    + "-" * 40
                )

            self.text_area.setPlainText("\n\n".join(lines))
            self.status_label.setText("Posts loaded successfully.")
            self.status_label.setStyleSheet("color: green; margin: 10px;")

        except IllegalAccessException:
            self.text_area.setPlainText("")
            self.status_label.setText("Error: You must be logged in to list posts.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except NoCurrentBlogException:
            self.text_area.setPlainText("")
            self.status_label.setText("Error: You must select a current blog first.")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
        except Exception as e:
            self.text_area.setPlainText("")
            self.status_label.setText(f"Error listing posts: {str(e)}")
            self.status_label.setStyleSheet("color: red; margin: 10px;")
