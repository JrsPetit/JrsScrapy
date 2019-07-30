import re
import urlparse
import urllib2
import time
import datetime
import robotparser
import threading
import multiprocessing
from JrsDownload import Downloader
from JrsSequential import JrsCallback
from JrsDBCache import MongoCache
from JrsDBQueue import MongoQueue
from pprint import pprint

SLEEP_TIME = 1

def thread_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None, num_retries=1, scrape_callback=None, cache=None,max_threads=10):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = MongoQueue()
    if cache == None:
        cache = MongoCache()
    crawl_queue.push(seed_url)

    # track how many URL's have been downloaded

    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while crawl_queue:
            url = crawl_queue.pop()
            print 'url in crawler.queue:',url
           
            html = D(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
                for link in links:
                    link = normalize(seed_url, link)
                    crawl_queue.push(link)
            crawl_queue.complete(url)

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)

def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print 'Starting {} processing'.format(num_cpus)
    processes = []
    for i in range(2):
        p = multiprocessing.Process(target=thread_crawler,args=[args],kwargs=kwargs)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)



if __name__ == '__main__':
    #link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    #link_crawler('http://example.webscraping.com', '/places/default/(index|view)', delay=0, num_retries=1, max_depth=1, user_agent='GoodCrawler',cache= MongoCache())
    begin = time.time()
    scrape_callback = JrsCallback()
    process_crawler(scrape_callback.seed_url, user_agent='jrs', scrape_callback= scrape_callback, max_depth=1)
    end = time.time()
    print 'total times : %.2f seconds' % (end - begin) 
    '''
    100 urls
    multi-threads:195.73s
    sequential:1660.47s
    2 process 10 threads:208.40, but too much time to raise keyError
    '''

    '''
    2019.7.20 can't pickle thread.lock objects
    can't pass cache = mongocache()  to multiprocess
    '''