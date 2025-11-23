import json
from blogging.blog import Blog


class BlogDecoder(json.JSONDecoder):
    def __init__(self):
        #turn dictionaries into real Blog objects
        super().__init__(object_hook=self.dict_to_object)
    
    def dict_to_object(self, d):
        # check if this dictionary is actually a Blog.
        if '_class_' in d and d['_class_'] == 'Blog':
            # Convert dictionary to Blog object
            blog = Blog(
                d['blog_id'],
                d['name'], 
                d['url'],
                d['email']
            )
            return blog
        # If the dictionary is not a Blog object, return it untouched
        return d