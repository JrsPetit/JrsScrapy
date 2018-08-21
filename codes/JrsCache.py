import urllib2
import urlparse
import random
import time
from datetime import datetime
import socket
import robotparser

DEFAULT_AGENT = 'jrs'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
        
    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()

class Downloader:
    def __init__(self,delay=DEFAULT_DELAY,user_agent=DEFAULT_AGENT,proxies=None,num_retries=DEFAULT_RETRIES,cache=None,opener=None,timeout=DEFAULT_TIMEOUT):
        socket.setdefaulttimeout(60)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache
        self.opener = opener
    
    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                #url is not available in cache
                pass
            else:
                if self.num_retries >0 and 500<= result['code'] <600:
                    #serve error so ignore result from cache and re-download
                    result = None
        
        if result is None:
            #result was not loaded from cache so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent':self.user_agent}
            result = self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                #save result to cache
                self.cache[url] = result
        return result['html']

    def download(self,url,headers,proxy,num_retries,data=None):
        print 'Downloading:', url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print 'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    return self._get(url, headers, proxy, num_retries-1, data)
                    #return download(self,url, headers, proxy, num_retries-1, data)
            else:
                code = None
        return {'html':html,'code':code}

def link_crawler(seed_url,link_regex=None,delay=DEFAULT_DELAY,max_depth=-1,max_url=-1,headers=None,user_agent=DEFAULT_AGENT,proxies=None,num_retries=-1,cache=None):
    crawl_queue = [seed_url]
    seen = {seed_url:0}
    num_urls = 0
    rp = get_robots(seed_url)
    D =Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_retries=num_retries,cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent,url):
            html = D(url)
            links = []


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp
