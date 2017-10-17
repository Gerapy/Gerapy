# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider as BaseSpider, signals
from scrapy_splash import SplashRequest
from scrapy import Request


class CrawlSpider(BaseSpider):
    name = None
    
    def start_requests(self):
        self.crawler.signals.connect(self.make_requests, signal=signals.spider_idle)
        return []
    
    def make_requests(self):
        for request in self.start():
            self.crawler.engine.slot.scheduler.enqueue_request(request)
    
    def start(self):
        for url in self.make_start_urls():
            yield Request(url)
    
    def make_start_urls(self):
        return self.start_urls
    
    def splash_request(self, request, args={'wait': 1}):
        meta = request.meta
        meta.update({'url': request.url})
        return SplashRequest(url=request.url, dont_process_response=True, args=args, callback=request.callback,
                             meta=meta)
    
    def _requests_to_follow(self, response):
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)
