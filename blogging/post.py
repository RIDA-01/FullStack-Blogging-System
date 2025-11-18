import datetime


class Post:
   
    
    def __init__(self, post_id, title, text):
        # Core post content and identity
        self.post_id = post_id
        self.title = title
        self.text = text
        # Timestamps required by assignment specification
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at  # Initially same as creation time
    
    def __eq__(self, other):
        """
        Compare posts for equality based on ID, title, and content.
        Used by tests to verify post data matches expected values.
        """
        return (
            isinstance(other, Post)
            and self.post_id == other.post_id
            and self.title == other.title
            and self.text == other.text
        )
    
    def update(self, title, text):
        """
        Update post content and refresh the update timestamp.
        """
        self.title = title
        self.text = text
        self.updated_at = datetime.datetime.now()
    
    def __str__(self):
        """
        User-friendly string representation
        """
        return f"Post #{self.post_id}: {self.title}"
    
    def __repr__(self):
        """
        Developer-friendly detailed representation
        """
        return f"Post(id={self.post_id}, title='{self.title}', created={self.created_at})"