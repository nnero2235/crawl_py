#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
the rcrawler use redis to manager task queue and url set.
so it will run faster. And become more easy.
but rcrawler dependency redis. so redis server must be started.
"""

import urllib.request
import datetime
import time
import logging
import random
import redis
from threading import Lock
from threading import Condition
from bs4 import BeautifulSoup

try:
    import threadPool
    import Cons
except:
    from . import threadPool
    from . import Cons

class NoURLError(Exception):
    def __init__(self):
        self.value = "No url in queue exits"
    def __str__(self):
        self.__repr__(self.value)

class Crawler(object):
    def __init__(self,startURL=None,baseURL=None,maxThreads=1,logLevel=10,projectName=None):
        self.__pool = threadPool.TinyThreadPool(maxThreads)
        self.startURL = startURL
        self.baseURL = baseURL
        self.redisPool = None
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.noURLError = NoURLError()
        self.projectName = projectName
        if self.projectName is None:
            raise RuntimeError("projectName must be a unique value to create redis taskQueue and urlSet")
        self.taskKey = self.projectName+":task_queue"
        self.urlKey = self.projectName+":url_set"
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',level=logLevel)

    def __fetchURL(self,url):
        logging.debug("Fetching:"+url)
        host = url[url.index("/")+2:url.index("/",8)]
        logging.debug("host:"+host)
        headers = {Cons.HTTP_HEADERS["ua"]:Cons.USER_AGENTS[random.randint(0,4)],
                    Cons.HTTP_HEADERS["host"]:host,
                    Cons.HTTP_HEADERS["refer"]:host}
        req = urllib.request.Request(url,headers=headers)

        try:
            resq = urllib.request.urlopen(req,timeout=30)
            code = resq.code
            if code == 200:
                result = resq.read().decode("utf-8")
                logging.info("200:"+url)
                return result
            else:
                logging.error("unexcepted Error code:"+code+" url:"+url)
        except:
            self.redisPool.lpush(self.taskKey,url)
            logging.error("timeout:"+url)
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

    def crawlURL(self,url):
        html = self.__fetchURL(url)
        if html is not None:
            soup = BeautifulSoup(html,"lxml")
            links = self.__getLinks(soup)
            for link in links:
                self.redisPool.lpush(self.taskKey,link)
            with self.condition:
                self.condition.notify()
            self.processData(soup)
        else:
            logging.info("html none:"+url)
        time.sleep(1)

    def processData(self,soup):
        raise NotImplementedError("must override processData method")

    def filterLink(self,link):
        raise NotImplementedError("must override filterLink method")

    def confRedis(self,host="localhost",port=6379,db=1,auth="nnero"):
        try:
            self.redisPool = redis.Redis(host=host,port=port,db=db,password=auth)
            if not self.redisPool.sismember(Cons.REDIS_TASK_KEYS,self.taskKey):
                self.redisPool.sadd(Cons.REDIS_TASK_KEYS,self.taskKey)
            if not self.redisPool.sismember(Cons.REDIS_URL_KEYS,self.urlKey):
                self.redisPool.sadd(Cons.REDIS_URL_KEYS,self.urlKey)

            self.redisPool.delete(self.taskKey)
            self.redisPool.delete(self.urlKey)
            self.redisPool.lpush(self.taskKey,self.startURL)
        except redis.ConnectionError:
            logging.error("redis connect failure please start redis server or check the auth!")
            exit(0)

    def start(self):
        if self.redisPool is None:
            raise RuntimeError("must be configure redis first.use \"confRedis\" method!")
        startTime = datetime.datetime.now()
        logging.critical("started!")
        while True:
            endTime = time.time() + Cons.TASK_QUEUE_WAIT_TIME
            url = self.redisPool.rpop(self.taskKey)
            try:
                while url is None:
                    with self.condition:
                        remaining = endTime - time.time()
                        if remaining <= 0.0:
                            raise self.noURLError
                        self.condition.wait(remaining)
                    url = self.redisPool.rpop(self.taskKey)
                    continue

                if self.redisPool.sismember(self.urlKey,url):
                    continue
                else:
                    self.redisPool.sadd(self.urlKey,url)
                url = url.decode("utf-8")
                self.__pool.execute(self.crawlURL,(url,))
            except NoURLError as e:
                logging.info(e.value)
                break
        self.__pool.join()
        # self.redisPool.shutdown()
        cost = datetime.datetime.now() - startTime
        logging.critical("finished!")
        logging.critical("cost:"+str(cost))
