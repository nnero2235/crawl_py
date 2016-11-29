#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-11-25 16:58:00
# Project: segment

import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://segmentfault.com/blogs?page=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        crawl_link(self,response)

    @config(priority=2)
    def detail_page(self, response):
        crawl_link(self,response)
        return {
            "url": response.url,
            "title": [x.text() for x in response.doc(".summary h2 a").items()],
        }

    def crawl_link(self,response):
        for each in response.doc('a[href^="http"]').items():
            if re.match(r"https://segmentfault.com/blogs\?page=\d+",each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
