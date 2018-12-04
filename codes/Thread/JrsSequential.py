# -*- coding: utf-8 -*-

import csv
from zipfile import ZipFile
from StringIO import StringIO
from JrsDownload import Downloader
from pprint import pprint

class JrsCallback:
    def __init__(self, max_urls = 10):
        self.max_urls = max_urls
        self.seed_url = 'http://127.0.0.1:8000/places/static/test.csv.zip'
    
    def __call__(self, url , html):
        if url == self.seed_url:
            urls = []
            with ZipFile(StringIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for _,website in csv.reader(zf.open(csv_filename)):
                    urls.append('http://' + website)
                    if len(urls) == self.max_urls:
                        break
            return urls

if __name__ == "__main__":
    D = Downloader()
    zipped_data = D('http://127.0.0.1:8000/places/static/test.csv.zip')
    urls = []
    with ZipFile(StringIO(zipped_data)) as zf:
        csv_filename = zf.namelist()[0]
        for _,website in csv.reader(zf.open(csv_filename)):
            urls.append('http://' + website)
            if len(urls) == 10:
                break
    for url in urls:
        pprint(url)