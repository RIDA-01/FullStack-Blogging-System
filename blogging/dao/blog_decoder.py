import json
from blogging.blog import Blog


class BlogDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)
    
    def dict_to_object(self, d):
        if '_class_' in d and d['_class_'] == 'Blog':
            # Convert dictionary back to Blog object
            blog = Blog(
                d['blog_id'],
                d['name'], 
                d['url'],
                d['email']
            )
            # Reset post_counter to 1 when loading from file
            # (posts will be loaded separately by PostDAOPickle)
            blog.post_counter = 1
            return blog
        return d