class Post:
    def __init__(self, post_id, title, text):
        self.post_id = post_id
        self.title = title
        self.text = text
    
    def __eq__(self, other):
        return (
            isinstance(other, Post)
            and self.post_id == other.post_id
            and self.title == other.title
            and self.text == other.text
        )