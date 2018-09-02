import os
import re
import urlparse

class DiskCache:
    def __init__(self,cache_dir='cache'):
        self.cache_dir = cache_dir
        #self.max_length = max_length
    
    def urlToPath(self,url):
        """Create file system path for this URL
        """
        components = urlparse.urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path +='index.html'
        filename = components.netloc + path + components.query
        #replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]','_',filename)
