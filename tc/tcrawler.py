#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import threadPool
import datetime
import time
import logging
import random
import queue
import tSet
from bs4 import BeautifulSoup

#same to logging LEVEL  value
LOG_DEBUG = 10
LOG_INFO = 20
LOG_WARNING = 30
LOG_ERROR = 40
LOG_CRITIAL = 50

USER_AGENTS = [
"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
]

class Crawler(object):
    def __init__(self,startURL=None,baseURL=None,maxThreads=1,logLevel=10):
        self.__pool = threadPool.TinyThreadPool(maxThreads)
        self.startURL = startURL
        self.baseURL = baseURL
        self.queue = queue.Queue(1000)
        self.queue.put(startURL)
        self.t_set = tSet.TSet()
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',level=logLevel)

    def __fetchURL(self,url):
        logging.debug("Fetching:"+url)
        headers = {"userAgent":USER_AGENTS[random.randint(0,4)]}
        req = urllib.request.Request(url,headers=headers)
        resq = urllib.request.urlopen(req)
        code = resq.code
        if code == 200:
            try:
                result = resq.read().decode("utf-8")
                logging.info("200:"+url)
                return result
            except: #may decode error
                return None
        elif code == 404:
            logging.error("404:"+url)
        elif code == 500 or code == 502 or code == 503:
            logging.error("Server Error:"+url)
        elif code == 403:
            logging.error("403 ip ban:"+url)
        else:
            logging.error("unexcepted Error code:"+code+" url:"+url)
        return None

    def __getLinks(self,soup=None):
        if soup is not None:
            urls = []
            a_tags = soup.select("a[href]")
            for tag in a_tags:
                link = tag.get("href")
                link = self.filterLink(link)
                if link is not None:
                    urls.append(link)

            return urls
        else:
            return None

    def crawlURL(self,url,queue):
        html = self.__fetchURL(url)
        if html is not None:
            soup = BeautifulSoup(html,"lxml")
            links = self.__getLinks(soup)
            for link in links:
                queue.put(link)
            self.processData(soup)
        else:
            logging.info("html none:"+url)
        time.sleep(1)

    def processData(self,soup):
        raise NotImplementedError("must override processData method")

    def filterLink(self,link):
        raise NotImplementedError("must override filterLink method")

    def start(self):
        startTime = datetime.datetime.now()
        logging.critical("started!")
        while True:
            try:
                url = self.queue.get(timeout=30)
                if self.t_set.contains(url):
                    continue
                else:
                    self.t_set.add(url)
                self.__pool.execute(self.crawlURL,(url,self.queue))
            except queue.Empty:
                logging.critical("no url in queue exit!")
                break
        self.__pool.join()
        cost = datetime.datetime.now() - startTime
        logging.critical("finished!")
        logging.critical("cost:"+str(cost))
