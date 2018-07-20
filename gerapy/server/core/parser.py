import os
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.settings.deprecated import check_deprecated_settings
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.utils.spider import iterate_spider_output
from twisted.internet import reactor
from gerapy.server.core.utils import process_request, process_response, process_item


class SpiderParser():
    items = []
    requests = []
    response = None
    
    def __init__(self, settings, spider, args):
        """
        init parser
        :param settings:
        :param spider:
        :param args:
        """
        self.args = args
        self.spider = spider
        self.crawler_process = CrawlerRunner(settings)
        self.spider_loader = self.crawler_process.spider_loader
        self.spidercls = self.spider_loader.load(self.spider)
    
    def get_callback(self, request):
        """
        get callback from obj or rules
        :param request:
        :return:
        """
        if getattr(self.spidercls, 'rules', None):
            rules = self.spidercls.rules
            rule_index = request.meta.get('rule', -1)
            if rule_index >= 0 and rule_index < len(rules):
                rule = rules[rule_index]
                return rule.callback
            for rule in rules:
                if rule.link_extractor.matches(request.url):
                    return rule.callback
        return 'parse'
    
    def run_callback(self, response, cb):
        """
        run callback and get items and requests
        :param response:
        :param cb:
        :return:
        """
        items, requests = [], []
        for x in iterate_spider_output(cb(response)):
            if isinstance(x, (BaseItem, dict)):
                items.append(x)
            elif isinstance(x, Request):
                requests.append(x)
        return items, requests
    
    def prepare_request(self, spider, request, args):
        """
        get request
        :param spider:
        :param request:
        :param args:
        :return:
        """
        
        def callback(response):
            """
            callback
            :param response:
            :return:
            """
            request = response.request
            cb = self.args.callback or 'parse'
            if not callable(cb):
                cb_method = getattr(spider, cb, None)
                if callable(cb_method):
                    cb = cb_method
            items, requests = self.run_callback(response, cb)
            
            # process request callback
            for request in requests:
                request.callback = self.get_callback(request)
                request.meta['callback'] = request.callback
            # process items and requests and response
            self.items += list(map(lambda item: process_item(item), items))
            self.requests += list(map(lambda request: process_request(request), requests))
            self.response = process_response(response)
        
        if args.meta:
            request.meta.update(args.meta)
        
        # update callback
        request.meta['callback'] = request.callback
        request.callback = callback
        return request
    
    def run(self):
        """
        run main
        :return:
        """
        request = Request(self.args.url, None)
        start_requests = lambda spider: [self.prepare_request(spider, request, self.args)]
        self.spidercls.start_requests = start_requests
        self.crawler_process.crawl(self.spidercls)
        if not len(self.crawler_process.crawlers) > 0:
            return {'ok': False}
        # init pcrawler
        self.pcrawler = list(self.crawler_process.crawlers)[0]
        d = self.crawler_process.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        return {
            'items': self.items,
            'requests': self.requests,
            'response': self.response,
            'ok': True
        }


def get_follow_requests_and_items(project_path, spider_name, args):
    """
    get follows
    :param project_path:
    :param spider_name:
    :param args:
    :return:
    """
    work_cwd = os.getcwd()
    try:
        os.chdir(project_path)
        settings = get_project_settings()
        check_deprecated_settings(settings)
        sp = SpiderParser(settings, spider_name, args)
        results = sp.run()
        return results
    finally:
        os.chdir(work_cwd)


def get_start_requests(project_path, spider_name):
    """
    get start requests
    :param project_path: project path
    :param spider_name: spider name
    :return:
    """
    work_cwd = os.getcwd()
    try:
        # change work dir
        os.chdir(project_path)
        # load settings
        settings = get_project_settings()
        check_deprecated_settings(settings)
        runner = CrawlerRunner(settings=settings)
        # add crawler
        spider_cls = runner.spider_loader.load(spider_name)
        runner.crawl(spider_cls)
        # get crawler
        crawler = list(runner.crawlers)[0]
        # get spider by crawler
        spider = crawler.spider
        # get start requests
        requests = list(spider.start_requests())
        if not requests and hasattr(spider, 'start'):
            requests = list(spider.start())
        requests = list(map(lambda r: process_request(r), requests))
        return {'finished': True, 'requests': requests}
    finally:
        os.chdir(work_cwd)
