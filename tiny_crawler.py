#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#test data:
# 1.single thread fetchs 554 pages costing 20min14s
# 2.multi thread(4) fetchs 554 pages costing 4min10s
# 3.multi process(2: my computer is 2 cores) fetchs 554 pages costing over 4min. I can't test because of sync set failed.
import urllib.request
import multiprocessing
import queue
import random
import time
import datetime
import re
from threading import Thread
from threading import Lock
from bs4 import BeautifulSoup

USER_AGENTS = [
"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
]

rootURL = "https://segmentfault.com"

setLock = Lock()
process_lock = multiprocessing.Lock()

class Worker(Thread):
    def __init__(self,queue,s):
        Thread.__init__(self)
        self.q = queue
        self.s = s

    def run(self):
        while True:
            url = self.q.get()
            if url in self.s:
                self.q.task_done()
                continue
            else:
                setLock.acquire()
                self.s.add(url)
                setLock.release()
            crawlURL(url,self.q,extractData)
            time.sleep(1)
            self.q.task_done()

def extractData(html=None):
    pass

def extractURL(htmlReal=None):
    soup = BeautifulSoup(htmlReal,"lxml")
    matchedURLs = []
    if soup is not None:
        urls = soup.select("a[href]")
        for url in urls:
            urlStr = url.get("href")
            if re.match(r"/blogs\?page=\d+",urlStr):
                matchedURLs.append(rootURL+urlStr)
    return matchedURLs

def fetchURL(url=None):
    headers = {"userAgent":USER_AGENTS[random.randint(0,4)]}
    req = urllib.request.Request(url,headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        code  = resp.code
        if code == 200:
            print("200 Fetch Success:"+url)
            return resp.read().decode("utf-8")
        elif code == 404:
            print("404 No such Page:"+url)
            return None
        elif code == 500 or code == 502 or code ==504:
            print("5xx Server Error:"+url)
            return None
        else:
            print("unexcepted Error code:"+code+" url:"+url)
            return None
    except:
        print("unexcepted Error!")
        return None

def crawlURL(url=None,queue=None,callback=None):
    html = fetchURL(url)
    if html is not None:
        urlList = extractURL(html)
        for newURL in urlList:
            queue.put(newURL)
        if callback is not None:
            callback(html)

def process_crawl(queue,s):
    while True:
        url = queue.get()
        if url in s:
            queue.task_done()
            continue
        else:
            process_lock.acquire()
            s.add(url)
            process_lock.release()
        crawlURL(url,queue,extractData)
        time.sleep(1)
        queue.task_done()

def thread_main():
    print("started!")
    start_time = datetime.datetime.now()
    start_url = "https://segmentfault.com/blogs"
    s = set()
    q = queue.Queue()
    q.put(start_url)

    for x in range(4):
        worker = Worker(q,s)
        worker.setDaemon(True)
        worker.start()

    q.join()
    cost = (datetime.datetime.now() - start_time);
    print("cost:"+str(cost))
    print("finished!")

def process_main():
    print("started!")
    start_time = datetime.datetime.now()
    start_url = "https://segmentfault.com/blogs"
    # pool = multiprocessing.Pool(2)
    s = set()
    q = multiprocessing.JoinableQueue(1000)
    q.put(start_url)

    for x in range(2):
        p = multiprocessing.Process(target=process_crawl,args=(q,s))
        p.start()

    # pool.close()
    # pool.join()
    q.join()
    cost = (datetime.datetime.now() - start_time);
    print("cost:"+str(cost))
    print("finished!")

if __name__ == "__main__":
    process_main()
