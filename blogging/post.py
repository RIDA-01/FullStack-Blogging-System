# class Post:
#     def __init__(self, post_id, title, text):
#         self.post_id = post_id
#         self.title = title
#         self.text = text
    
#     def __eq__(self, other):
#         return False  
    
from datetime import datetime

class Post:
    def __init__(self, post_id, title, text, created_at=None, updated_at=None):
        self.post_id = post_id
        self.title = title
        self.text = text
        now = datetime.now()
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def __eq__(self, other):
        if not isinstance(other, Post):
            return False
        # tests compare by id, title, text (not timestamps)
        return (self.post_id == other.post_id and
                self.title == other.title and
                self.text == other.text)

    def __str__(self):
        return f"Post({self.post_id}): {self.title}"
