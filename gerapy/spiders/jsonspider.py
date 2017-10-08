# -*- coding: utf-8 -*-
import json
from scrapy.utils.python import unique as unique_list
from scrapy.link import Link
from scrapy.spiders import CrawlSpider as BaseSpider, signals


class JsonLinkExtractor():
    def __init__(self, patterns):
        self.patterns = patterns
    
    def get_value(self, dict, *keys):
        if len(keys) == 1:
            return dict.get(keys[0])
        else:
            result = []
            for key in keys:
                result.append(dict.get(key))
        return result
    
    def get_slice(self, list, start, end=None):
        if start == '*':
            return list
        else:
            return list[start:end]
    
    def extract_links(self, response):
        result = json.loads(response.text)
        for pattern in self.patterns:
            extractors = pattern.get('extractors')
            format = pattern.get('format')
            data = result
            for extractor in extractors:
                type = extractor.get('type')
                if isinstance(data, dict):
                    if type == 'value':
                        data = self.get_value(*([data] + extractor.get('args')))
                elif isinstance(data, list):
                    if type == 'value':
                        data = [self.get_value(*([item] + extractor.get('args'))) for item in data]
                    elif type == 'slice':
                        data = self.get_slice(*([data] + extractor.get('args')))
            if not isinstance(data, list):
                data = [data]
            all_links = [Link(response.urljoin(format.format(*[item]))) if not isinstance(item, list) else
                         Link(response.urljoin(format.format(*item))) for item in data]
            return unique_list(all_links)


class JsonSpider(BaseSpider):
    name = None
    
    def start_requests(self):
        self.crawler.signals.connect(self.make_requests, signal=signals.spider_idle)
        return []
    
    def make_requests(self):
        for request in self.start():
            self.crawler.engine.slot.scheduler.enqueue_request(request)
    
    def start(self):
        raise NotImplementedError
    
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
