#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import datetime
import time
from lxml import etree
import redis

r = redis.Redis("localhost",port=6379,db=1,password="nnero")
url = "https://segmentfault.com/blogs";
user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)";

headers = {"user_agent":user_agent}

def extractQuestion(html):
    doc = etree.HTML(html)
    if doc != None:
        titles = doc.cssselect("div.summary h2 a")
        for e in titles:
            r.lpush("question",e.text)

def downloadURL(url,callback=None):
    req = urllib.request.Request(url,None,headers)
    resp = urllib.request.urlopen(req)
    code = resp.code
    if code == 200:
        print("Download:"+url+" sucess!")
        if callback != None:
            callback(resp.read().decode("utf-8"))
        return True
    elif code == 500:
        print("Download:"+url+" failure!")
        return True
    elif code == 404:
        print("404 get.")
        return True
    else:
        print("unexcept error:"+str(i))
        return True

i = 1
start_time = datetime.datetime.now()
while(downloadURL(url+"?page="+str(i),extractQuestion)):
    i+=1
    time.sleep(1)
    if i == 50:
        break
r.client_kill()
cost = (datetime.datetime.now() - start_time);
print("costReal:"+"secs:"+str(cost))
