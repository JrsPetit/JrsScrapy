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

class JrsBrowser(QWebView):
    def __init__(self, display = True):
        self.app = QApplication([])
        QWebView.__init__(self)
        if display:
            self.show() #show the browser

    def download(self, url, timeout = 60):
        """wait for download to complete and return result"""
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout * 1000)
        loop.exec_() #delay here until download finished
        if timer.isActive():
            #downloaded successfully
            timer.stop()
            return self.html()
        else:
            #time out
            print "Request timed out: "+url
    
    def html(self):
        """Shortcut to return the current HTML"""
        return self.page().mainFrame().toHtml()
    
    def find(self, pattern):
        """Find all elements that match the pattern"""
        return self.page().mainFrame().findAllElements(pattern)
    
    def attr(self, pattern, name, value):
        """Set attribute for matching elements"""
        for e in self.find(pattern):
            e.setAttribute(name, value)

    def text(self, pattern, value):
        """Set attribute for matching elements"""
        for e in self.find(pattern):
            e.setPlainText(value)
    
    def click(self, pattern):
        """Click matching elements"""
        for e in self.find(pattern):
            e.evaluateJavaScript("this.click()")

    def wait_load(self, pattern, timeout=60):
        """Wait for this pattern to be found in webpage and return matches"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print 'Wait load timed out'    


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
    """ url = "http://192.168.0.103:8000/places/default/search"
    app = QApplication([])
    webview = QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl(url))
    loop.exec_()
    webview.show()
    frame = webview.page().mainFrame()
    frame.findFirstElement('#search_term').setAttribute('value','.')
    #frame.findFirstElement('#page_size option:checked').setPlainText('150')
    for e in frame.findAllElements('#page_size option'):
        e.setPlainText('15')
    #frame.findallElement('#page_size option:checked').setAttribute('value','15')
    frame.findFirstElement('#search').evaluateJavaScript('this.click()')
    elements = None
    while not elements:
        app.processEvents()
        elements = frame.findAllElements('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    print countries
    app.exec_() """

    br = JrsBrowser()
    br.download('http://192.168.0.103:8000/places/default/search')
    br.attr('#search_term','value','.')
    br.text('#page_size option','1000')
    br.click('#search')
    elements = br.wait_load('#results a')
    for e in elements:
        print e.toPlainText().strip()
    br.app.exec_()
    #countries = [e.ttoPlainText().strip()oPlainText().strip() for e in elements]
    #pprint(elements)