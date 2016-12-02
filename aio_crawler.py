#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import async_timeout
import queue
import time
import datetime
from bs4 import BeautifulSoup
import re

USER_AGENTS = [
"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
]

rootURL = "https://segmentfault.com"

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

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def crawlURL(loop,queue,s,callback=None):
    while True:
        url = queue.get()
        if url in s:
            continue
        else:
            s.add(url)
        async with aiohttp.ClientSession(loop=loop) as session:
            html = await fetch(session, url)
            if html is not None:
                urlList = extractURL(html)
                for newURL in urlList:
                    queue.put(newURL)
                if callback is not None:
                    callback(html)
                # time.sleep(1)
def main():
    print("started!")
    start_time = datetime.datetime.now()
    start_url = "https://segmentfault.com/blogs"
    s = set()
    q = queue.Queue()
    q.put(start_url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawlURL(loop,q,s,extractData))
    loop.close()
    cost = (datetime.datetime.now() - start_time);
    print("cost:"+str(cost))
    print("finished!")

if __name__ == "__main__":
    main()
