import urllib2
import urlparse
import random
import time
from datetime import datetime
import socket
import robotparser
import re

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

def link_crawler(seed_url,link_regex=None,delay=DEFAULT_DELAY,max_depth=-1,max_urls=-1,headers=None,user_agent=DEFAULT_AGENT,proxies=None,num_retries=-1,scrape_callback=None,cache=None):
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
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])

            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url

def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)

def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc
def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp

def get_links(html):
    print 1111
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/places/static'
    rp = robotparser.RobotFileParser()
    rp.set_url('http://127.0.0.1:8000/places/static/robots.txt')
    #rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    print urlparse.urljoin(url, '/robots.txt')
    rp.read()
    print rp
    url1 = 'http://127.0.0.1:8000/places'
    #user_agent = 'jrs'
    user_agent = 'BadCrawler'
    print rp.can_fetch(user_agent,url1)

    url2 = "http://example.webscraping.com/default/view/Australia-1"
    print re.sub('[^/0-9a-zA-Z\-.,;_ ]','_',url2)
