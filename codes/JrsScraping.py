import re
import urllib2
from bs4 import BeautifulSoup

def download(url):
    return urllib2.urlopen(url).read()

if __name__ == "__main__":
    url = 'http://127.0.0.1:8000/places/default/view/Aland-Islands-2'
    html = download(url)
    print re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>',html)
    #print re.findall('<td class="w2p_fw">(.*?)</td>',html)[1]

    soup = BeautifulSoup(html,"html.parser")
    tr = soup.find(attrs={'id':'places_area__row'})
    td = tr.find(attrs={'class':'w2p_fw'})
    print td.text