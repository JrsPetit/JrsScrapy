import urllib2
import re
import itertools
import urlparse

def download(url,user_agent = 'jrs',num_retries = 2):
    print 'Downloading:',url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers=headers)
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
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        links = get_links(html)
        for link in links:
            if re.match(link_regex ,link):
                link = urlparse.urljoin(seed_url, link)
                crawl_queue.append(link)
                print 2222
            else:
                print link

def get_links(html):
    print 1111
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

link_crawler('http://example.webscraping.com', '/places/default/(index|view)')
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
