import re
import urllib2
import lxml.html
from bs4 import BeautifulSoup
import time

FIELDS = ('area','population','iso','country','capital','continent','tld','currency_code','currency_name','phone','postal_code_format','postal_code_regex','languages','neighbours')
NUM_ITERATIONS = 100 #number of times to test each scraper
def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search(r'<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results

def bs_scraper(html):
    soup = BeautifulSoup(html,'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr',id='places_%s__row' % field).find('td',class_='w2p_fw').text
    return results

def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table>tr#places_%s__row>td.w2p_fw' % field)[0].text_content()
    return results

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

    for name,scraper in [('Regular expressions',re_scraper),('BeautifulSoup',bs_scraper),('lxml',lxml_scraper)]:
        start_time = time.time()
        for i in range(NUM_ITERATIONS):
            if scraper == re_scraper:
                re.purge()
            result = scraper(html)
            assert(result['area'] =='1580 square kilometres')
        end = time.time()
        print '%s:%.2f seconds' % (name,end-start_time)
#2018.08.05 test
'''
1580 square kilometres
Regular expressions:15.61 seconds
BeautifulSoup:77.98 seconds
lxml:3.76 seconds
'''