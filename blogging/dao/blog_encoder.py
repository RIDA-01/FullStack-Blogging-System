import json 
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    def default(self, obj):
        print(f"Encoding object: {type(obj)}")
        if isinstance(obj, Blog):
            # Convert Blog object to dictionary
            result = {
                'blog_id': obj.blog_id,
                'name': obj.name,
                'url': obj.url,
                'email': obj.email,
                # 'post_counter': obj.post_counter,
                '_class_': 'Blog'
            }
            print(f"Encoded blog: {result}")
            return result
        print(f"Using default encoder for: {type(obj)}")
        return super().default(obj)