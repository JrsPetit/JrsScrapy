import re
import urllib2
from bs4 import BeautifulSoup

def download(url,user_agent = 'jrs',num_retries = 2):
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers=headers)
    try:
        print 'Downloading ',url
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries >0:
            if hasattr(e,'code') and 500<= e.code <600:
                return download(url,user_agent,num_retries-1)
    return html

if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/places/default/view/Aland-Islands-2'
    html = download(url)
    print re.findall(r'<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>',html)
    #print re.findall('<td class="w2p_fw">(.*?)</td>',html)[1]

    soup = BeautifulSoup(html,"html.parser")
    tr = soup.find(attrs={'id':'places_area__row'})
    td = tr.find(attrs={'class':'w2p_fw'})
    print td.text