#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread,Lock,Condition

WORKER_READY = 1
WORKER_RUNNING = 2
WORKER_FINISHED = 3


class TinyThreadPool(object):
    def __init__(self,num=1):
        self.maxNum = num
        self.runningWorker = AtomWorkerCount()
        self.mutex = Lock()
        self.full = Condition(self.mutex)

    def execute(self,func=None,args=()):
        if func is None:
            return

        if self.runningWorker.get() >= self.maxNum:
            with self.full:
                self.full.wait()

        self.runningWorker.atomIncrement()
        worker = Worker(func,args,self.full,self.runningWorker)
        # worker.setDaemon(True)
        worker.start()

    def join(self):
        while self.runningWorker.get() != 0:
            pass

class Worker(Thread):
    def __init__(self,func=None,args=(),fullLock=None,runningWorker=None):
        Thread.__init__(self)
        self.runningWorker = runningWorker
        self.func = func
        self.args = args
        self.status = WORKER_READY
        self.fullLock = fullLock

    def run(self):
        self.status = WORKER_RUNNING
        self.func(*self.args)
        self.status = WORKER_FINISHED
        self.runningWorker.atomDescrement()
        with self.fullLock:
            self.fullLock.notify()

    def getStatus(self):
        return self.status

class AtomWorkerCount(object):
    def __init__(self):
        self.count = 0
        self.workerCountLock = Lock()

    def atomIncrement(self):
        self.workerCountLock.acquire()
        self.count += 1
        self.workerCountLock.release()

    def atomDescrement(self):
        self.workerCountLock.acquire()
        self.count -= 1
        self.workerCountLock.release()

    def get(self):
        return self.count
