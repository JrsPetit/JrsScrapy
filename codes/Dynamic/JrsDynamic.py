# -*- coding: utf-8 -*-
import lxml.html
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
    writer = csv.writer(open('countries.csv','w'))
    writer.writerow(FIELDS)
    D = Downloader()
    url = "http://192.168.0.103:8000/places/ajax/search.json?search_term={}&page_size={}&page={}"
    html = D(url.format('.',1000,0))
    ajax = json.loads(html)
    for record in ajax['records']:
        row = [record[field] for field in FIELDS]
        writer.writerow(row)

if __name__ == "__main__":
    url = "http://192.168.0.103:8000/places/default/dynamic"
    app = QApplication([])
    webview = QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl(url))
    loop.exec_()
    html = webview.page().mainFrame().toHtml()
    tree = lxml.html.fromstring(html)
    print tree.cssselect('#result')[0].text_content()
    MyFun2()