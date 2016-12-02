#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock

class NQueue(object):
    def __init__(self):
        self.q = []
        self.size = 0
        self.lock = Lock()

    def put(self,item=None):
        if item is not None:
            self.lock.acquire()
            self.q.append(item)
            self.size += 1
            self.lock.release()

    def get(self,timeout=0):
        if self.size == 0:
            return None
        else:
            self.lock.acquire()
            item = self.q.pop(0)
            self.size -= 1
            self.lock.release()
            return item

    def size(self):
        return self.size
