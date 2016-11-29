import scrapy

class SegmentSpider(scrapy.Spider):
    name = "segments"

    def start_requests(self):
        urls = [
        "https://segmentfault.com/blogs?page=1",
        "https://segmentfault.com/blogs?page=2"
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,resp):
        titles = resp.css("div.summary h2 a::text")
        for e in titles:
            print(e.extract())
