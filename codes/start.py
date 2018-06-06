import urllib2
import re
import itertools
import urlparse
import robotparser

def download(url,user_agent = 'jrs',proxy=None,num_retries = 2):
    print 'Downloading:',url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers=headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download erro:',e.reason
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<= e.code < 600:
                return download(url,num_retries-1)
    return html

def link_crawler(seed_url, link_regex):
    """crawl from the given seed URL following links matched by link_regex
    """
    rp = robotparser.RobotFileParser()
    rp.set_url('http://192.168.1.5:8000/places/static/robots.txt')
    rp.read()
    user_agent = 'BadCrawler'

    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            html = download(url)
            links = get_links(html)
            for link in links:
                if re.match(link_regex ,link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
                else:
                    print 'do not want ',link
        else:
            print 'Blocked by robots.txt ',url 

def get_links(html):
    print 1111
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

link_crawler('http://192.168.1.5:8000/places', '/places/default/(index|view)')
'''
rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
url = 'http://example.webscraping.com'
user_agent = 'jrs'
print rp.can_fetch(user_agent,url)
'''
'''test_str = '/places/default/index'
test_regex = '/places/default/(index|view)' 
if re.match(test_regex ,test_str):
    print 'good'
else:
    print 'bad'
'''
'''
download('http://example.webscraping.com')
crawl_sitemap('http://example.webscraping.com/sitemap.xml')
'''
