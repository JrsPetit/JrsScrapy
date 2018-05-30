import urllib2

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
'''
download('http://example.webscraping.com')
'''
