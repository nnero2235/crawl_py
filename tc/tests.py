

import threadPool
import time
import unittest
import tcrawler
import re

def say(s):
    time.sleep(1)
    print(s)
    time.sleep(1)

class Segment(tcrawler.Crawler):

    def processData(self,soup):
        pass

    def filterLink(self,link):
        if re.match(r"/blogs\?page=\d+",link):
            return self.baseURL + link
        return None

class TestAll(unittest.TestCase):

    # def test_threadPool(self):
    #     pool = threadPool.TinyThreadPool(5)
    #     for x in range(100):
    #         pool.execute(say,("haha:"+str(x),))
    #     # time.sleep(10)
    #     pool.join()

    def test_segment(self):
        startURL = "https://segmentfault.com/blogs"
        baseURL = "https://segmentfault.com"
        c = Segment(startURL=startURL,baseURL=baseURL,maxThreads=10,logLevel=tcrawler.LOG_INFO)
        c.start()


if __name__ == "__main__":
    unittest.main()
