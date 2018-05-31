import urllib2
import re
import itertools

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

def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html = download(link)

#maxinum unmber of consecutive download errors allowed
max_errors = 5
#current number of consecutive download errors
num_errors = 0
for page in itertools.count(1,1):
    url = 'http://example.webscraping.com/view/-%d' % page
    html = download(url)
    if html is None:
        num_errors +=1
        if num_errors == max_errors:
            break
    else:
        num_errors = 0
'''
download('http://example.webscraping.com')
crawl_sitemap('http://example.webscraping.com/sitemap.xml')
'''
