
import queue
import threading

class Queue(object):
    def __init__(self):
        self.taskQueue = queue.Queue()
        self.fetchedSet = set()
        self.lock = threading.Lock()

    def push(self,item):
        try:
            self.lock.acquire()
            if item not in self.fetchedSet:
                self.fetchedSet.add(item)
                self.taskQueue.put(item)
        finally:
            self.lock.release()

    def poll(self):
        try:
            return self.taskQueue.get(timeout=30)
        except queue.Empty:
            return None

    def rePush(self):
        self.taskQueue.put(item)

    def getSetSize(self):
        return len(self.fetchedSet)
