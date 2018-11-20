# -*- coding: utf-8 -*-

import csv
from zipfile import ZipFile
from StringIO import StringIO
from JrsDownload import Downloader
from pprint import pprint

if __name__ == "__main__":
    D = Downloader()
    zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    urls = []
    with ZipFile(StringIO(zipped_data)) as zf:
        csv_filename = zf.namelist()[0]
        for _,website in csv.reader(zf.open(csv_filename)):
            urls.append('http://' + website)
    
    """ for url in urls:
        pprint(url) """