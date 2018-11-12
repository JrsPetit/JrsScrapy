# -*- coding: utf-8 -*-
import os
import re
import urlparse
import shutil
import zlib
from datetime import datetime, timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle
from JrsLinkCrawler import link_crawler
import time
class DiskCache:
    def __init__(self,cache_dir='JrsCache',expires=timedelta(days=30),compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress
        #self.max_length = max_length
     
    def __getitem__(self,url):
        """Load data from disk for this URL
        """
        path = self.urlToPath(url)
        if os.path.exists(path):
            with open(path,'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result,timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            #URL has not yet been cached
            raise KeyError(url + 'does not exist')
    
    def __setitem__(self,url,result):
        """save data to disk for this url
        """
        path = self.urlToPath(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print 'direrror:',str(e)
        data = pickle.dumps((result,datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path,'wb') as fp:
            fp.write(data)

    '''
    def __delitem__(self,url):
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError：
            pass

    def clear(self):
        if os.path.exists(self.cache_dir):
           shutil.retree(self.cache_dir) 
    '''


    def has_expired(self,timestamp):
        return datetime.utcnow() > timestamp + self.expires

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
        filename = re.sub(r'[^/0-9a-zA-Z\-.,;_ ]','_',filename)
        #restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        print 'filenames:',filename
        return os.path.join(self.cache_dir,filename)

if __name__ == '__main__':
    #link_crawler('http://127.0.0.1:8000/places/default/index/1', '/places/default/(index|view)', cache=DiskCache())
    cache = DiskCache(expires=timedelta(seconds=5))
    url = "http://127.0.0.1:8000/places/default/index/1"
    result = {'html':'...'}
    cache[url] = result
    print cache[url]
    time.sleep(5)
    print cache[url]

    """ paths =  'JrsCache2\\127.0.0.1_8000/places/default/index/1'  
    os.makedirs(paths)
    paths2 = 'JrsCache3\\127.0.0.1_8000/places/default/index/1'
    folders = os.path.dirname(paths2)
    os.makedirs(folders) """
    
    """ result = [0,1,2]
    JFilenames = '127.0.0.1_8000/places/default/index/1.txt'
    JPath = os.path.join('cache',JFilenames)
    print JPath
    JFolder = os.path.dirname(JPath)
    print JFolder
    if not os.path.exists(JFolder):
        os.makedirs(JFolder)
    with open(JPath,'wb') as fp:
        fp.write(pickle.dumps(result))
    if os.path.exists(JPath):
            with open(JPath,'rb') as fp:
                print pickle.load(fp)[2]
    else:
        #URL has not yet been cached
        raise KeyError('url' + 'does not exist') """

'''
import os
import re
import urlparse
import shutil
import zlib
from datetime import datetime, timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle
from link_crawler import link_crawler


class DiskCache:
    """
    Dictionary interface that stores cached 
    values in the file system rather than in memory.
    The file path is formed from an md5 hash of the key.

    >>> cache = DiskCache()
    >>> url = 'http://example.webscraping.com'
    >>> result = {'html': '...'}
    >>> cache[url] = result
    >>> cache[url]['html'] == result['html']
    True
    >>> cache = DiskCache(expires=timedelta())
    >>> cache[url] = result
    >>> cache[url]
    Traceback (most recent call last):
     ...
    KeyError: 'http://example.webscraping.com has expired'
    >>> cache.clear()
    """

    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        """
        cache_dir: the root level folder for the cache
        expires: timedelta of amount of time before a cache entry is considered expired
        compress: whether to compress data in the cache
        """
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    
    def __getitem__(self, url):
        """Load data from disk for this URL
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')


    def __setitem__(self, url, result):
        """Save data to disk for this url
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)


    def __delitem__(self, url):
        """Remove the value at this key and any empty parent sub-directories
        """
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass


    def url_to_path(self, url):
        """Create file system path for this URL
        """
        components = urlparse.urlsplit(url)
        # when empty path set to /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)


    def has_expired(self, timestamp):
        """Return whether this timestamp has expired
        """
        return datetime.utcnow() > timestamp + self.expires


    def clear(self):
        """Remove all the cached values
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=DiskCache())
'''