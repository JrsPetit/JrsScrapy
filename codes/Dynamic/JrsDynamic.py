# -*- coding: utf-8 -*-
import lxml.html
import re
from JrsDownload import Downloader
from pprint import pprint
import json
import string
import time
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
except ImportError:
    import PySide
import csv

def MyFun():
    D = Downloader()
    url = "http://192.168.0.103:8000/places/ajax/search.json?search_term={}&page_size={}&page={}"
    country = set()
    for letter in string.lowercase:
        page = 0
        pagesize = 10
        while True:
            html = D(url.format(letter,pagesize,page))
            try:
                ajax = json.loads(html)
            except ValueError as e:
                print e
                ajax = None
            else:
                for record in ajax['records']:
                    country.add(record['country'])
            page +=1
            if ajax is None or page >= ajax['num_pages']:
                break
    open('country.txt','w').write('\n'.join(sorted(country))) 

    #tree = lxml.html.fromstring(html)
    #tree = json.loads(html)
    #print tree['records'] 

def MyFun2():
    FIELDS= ('pretty_link','country','id','href','src')
    FIELDS2= ('pretty_link','country','id')
    writer = csv.writer(open('countries.csv','w'))
    writer.writerow(FIELDS)
    D = Downloader()
    url = "http://192.168.0.103:8000/places/ajax/search.json?search_term={}&page_size={}&page={}"
    html = D(url.format('.',1000,0))
    ajax = json.loads(html)
    for record in ajax['records']:
        row = [record[field] for field in FIELDS2]
        prelink = record['pretty_link']
        href_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        row.append(href_regex.findall(prelink)[0])
        img_regex = re.compile('<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
        row.append(img_regex.findall(prelink)[0])
        writer.writerow(row)
#"<div><a href=\"/places/default/view/Afghanistan-1\"><img src=\"/places/static/images/flags/af.png\" /> Afghanistan</a></div>"

if __name__ == "__main__":
    url = "http://192.168.0.103:8000/places/default/search"
    app = QApplication([])
    webview = QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl(url))
    loop.exec_()
    webview.show()
    frame = webview.page().mainFrame()
    frame.findFirstElement('#search_term').setAttribute('value','.')
    frame.findFirstElement('#page_size option:checked').setPlainText('1000')
    frame.findFirstElement('#search').evaluateJavaScript('this.click()')
    app.exec_()