#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
from lxml import etree
import queue
from concurrent.futures import ThreadPoolExecutor
import random
import time
import datetime
import re
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

def execCrawl(q=None,fetchedSet=None):
    try:
        url = q.get(timeout=60)
        if url in fetchedURLSet:
            return
        else:
            setLock.acquire()
            fetchedSet.add(url)
            setLock.release()
        crawlURL(url,q,extractData)
    except queue.Empty:
        pass

def main():
    print("started!")
    start_time = datetime.datetime.now()
    start_url = "https://segmentfault.com/blogs"
    executorPool= ThreadPoolExecutor(5)
    fetchedURLSet = set()
    q = queue.Queue(1000)
    q.put(start_url)
    while True:
        # try:
        #     url = q.get(timeout=60)
        #     if url in fetchedURLSet:
        #         continue
        #     else:
        #         fetchedURLSet.add(url)
        #     crawlURL(url,q,extractData)
        #     time.sleep(1)
        # except queue.Empty:
        #     break
            # if count == 1000:
                # print("No longer has url exit!")
                # break
            # count+=1
            # time.sleep(0.2)
        executorPool.submit(execCrawl,q,fetchedURLSet)
        time.sleep(1)
    executorPool.shutdown()
    cost = (datetime.datetime.now() - start_time);
    print("cost:"+str(cost))
    print("finished!")

if __name__ == "__main__":
    main()
