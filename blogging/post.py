class Post:
    def __init__(self, post_id, title, text):
        self.post_id = post_id
        self.title = title
        self.text = text
    
    def __eq__(self, other):
        # Check if other is a Post object
        if not isinstance(other, Post):
            return False

        # Compare attributes
        if self.post_id != other.post_id:
            return False
        if self.title != other.title:
            return False
        if self.text != other.text:
            return False

        # If all checks passed, they are equal
        return True

    
    def __repr__(self):
        return f"Post(post_id={self.post_id!r}, title={self.title!r})"

    def __str__(self):
        return f"[{self.post_id}] {self.title}"
