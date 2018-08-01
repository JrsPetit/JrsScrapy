import re
import urllib2
import lxml.html
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

    broken_html = "<ul class = country><li>Area<li>Population</ul>"
    tree = lxml.html.fromstring(broken_html)
    fixed_html = lxml.html.tostring(tree,pretty_print=True)
    print "new html:\n",fixed_html

    tree2 = lxml.html.fromstring(html)
    td = tree2.cssselect("tr#places_area__row > td.w2p_fw")[0]
    print td.text_content()