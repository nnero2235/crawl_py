#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from lxml import etree
# import gevent

url = "https://segmentfault.com/blogs";
user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)";

headers = {"user_agent":user_agent}

def extractQuestion(html):
    doc = etree.HTML(html)
    if doc != None:
        titles = doc.cssselect("div.summary h2 a")
        if titles is not None:
            print(titles[0].text)

def downloadURL(url,callback =None):
    req = urllib.request.Request(url,None,headers)
    resp = urllib.request.urlopen(req)
    code = resp.code
    if code == 200:
        print("Download:"+url+" sucess!")
        if callback != None:
            callback(resp.read().decode("utf-8"))
    else:
        print("unexcept error:"+str(i))


#scrpit run
i = 1
start_time = datetime.datetime.now()
#test single thread
# while(i < 100):
#     downloadURL(url+"?page="+str(i))
#     i+=1
#     time.sleep(1)

#test mutil thread
pool = ThreadPoolExecutor(5)
while(i<100):
    pool.submit(downloadURL,url+"?page="+str(i))
    i+=1
    time.sleep(1)
pool.shutdown()

#test mutil process
# pool = ProcessPoolExecutor(2)
# while(i<100):
#     pool.submit(downloadURL(url+"?page="+str(i)))
#     i+=1
#     time.sleep(1)

#test gevent
# threads = []
# for i in range(1,100):
#     threads.append(gevent.spawn(downloadURL,url+"?page="+str(i)))
# print("start")
# gevent.joinall(threads)

cost = (datetime.datetime.now() - start_time);
print("costReal:"+str(cost))
