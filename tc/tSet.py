
from threading import Lock

class TSet(object):

    def __init__(self):
        self.s = set()
        self.lock =Lock()

    def add(self,item):
        self.lock.acquire()
        self.s.add(item)
        self.lock.release()

    def contains(self,item):
        return item in self.s
