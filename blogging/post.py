from datetime import datetime

class Post:
    def __init__(self, post_id, title, text):
        self.post_id = post_id
        self.title = title
        self.text = text

        # timestamps: required by the spec (created now; updated starts the same)
        now = datetime.now()
        self.created_at = now
        self.updated_at = now

    def touch(self):
        """Update the timestamp when the post is edited."""
        self.updated_at = datetime.now()
    
    def __eq__(self, other):
        # Check if other is a Post object
        if not isinstance(other, Post):
            return False

        # Compare attributes that define logical equality for tests
        return (
            self.post_id == other.post_id and
            self.title == other.title and
            self.text == other.text
        )

    def __repr__(self):
        return f"Post(post_id={self.post_id!r}, title={self.title!r})"

    def __str__(self):
        return f"[{self.post_id}] {self.title}"
