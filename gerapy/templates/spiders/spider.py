# -*- coding: utf-8 -*-
from scrapy import Spider as BaseSpider, signals
from scrapy_splash import SplashRequest


class Spider(BaseSpider):
    name = None
    
    def start_requests(self):
        self.crawler.signals.connect(self.make_requests, signal=signals.spider_idle)
        return []
    
    def make_requests(self):
        for request in self.start():
            self.crawler.engine.slot.scheduler.enqueue_request(request)
    
    def start(self):
        raise NotImplementedError
    
    def splash_request(self, request, args={'wait': 1}):
        meta = request.meta
        meta.update({'url': request.url})
        return SplashRequest(url=request.url, dont_process_response=True, args=args, callback=request.callback,
                             meta=meta)
