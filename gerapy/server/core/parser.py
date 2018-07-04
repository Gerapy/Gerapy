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
        self.args = args
        self.spider = spider
        self.crawler_process = CrawlerRunner(settings)
        print('crawler_process', self.crawler_process)
        self.spider_loader = self.crawler_process.spider_loader
        print('spider_loader', self.spider_loader)
        self.spidercls = self.spider_loader.load(self.spider)
        print('spidercls', self.spidercls)
    
    def get_callback(self, request):
        if self.args.callback:
            return self.args.callback
        if request.callback:
            return request.callback.__name__
        if request.meta['callback']:
            return request.meta['callback']
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
        items, requests = [], []
        for x in iterate_spider_output(cb(response)):
            if isinstance(x, (BaseItem, dict)):
                items.append(x)
            elif isinstance(x, Request):
                requests.append(x)
        return items, requests
    
    def prepare_request(self, spider, request, args):
        def callback(response):
            request = response.request
            # determine real callback
            cb = self.get_callback(request)
            
            if not callable(cb):
                cb_method = getattr(spider, cb, None)
                if callable(cb_method):
                    cb = cb_method
            
            items, requests = self.run_callback(response, cb)
            
            # process request callback
            for request in requests:
                request.callback = self.get_callback(request)
                request.meta['callback'] = request.callback
            
            self.items += list(map(lambda item: process_item(item), items))
            self.requests += list(map(lambda item: process_request(item), items))
            self.response = process_response(response)
        
        if args.meta:
            request.meta.update(args.meta)
        
        request.meta['callback'] = request.callback
        request.callback = callback
        return request
    
    def run(self):
        request = Request(self.args.url, None)
        print(request)
        start_requests = lambda spider: [self.prepare_request(spider, request, self.args)]
        self.spidercls.start_requests = start_requests
        print('start_requests', start_requests)
        self.crawler_process.crawl(self.spidercls)
        print('Crawwwwwlers', self.crawler_process, self.crawler_process.crawlers)
        if not len(self.crawler_process.crawlers) > 0:
            return {'ok': False}
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
    work_cwd = os.getcwd()
    print('word', work_cwd)
    try:
        os.chdir(project_path)
        settings = get_project_settings()
        print('settings', settings)
        check_deprecated_settings(settings)
        sp = SpiderParser(settings, spider_name, args)
        
        results = sp.run()
        print(results)
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
    print('Word cwd', work_cwd)
    print('Project path', project_path)
    try:
        # change work dir
        os.chdir(project_path)
        # load settings
        settings = get_project_settings()
        check_deprecated_settings(settings)
        print(settings)
        runner = CrawlerRunner(settings=settings)
        # add crawler
        spider_cls = runner.spider_loader.load(spider_name)
        runner.crawl(spider_cls)
        print('Runner crawlers', runner.crawlers)
        # get crawler
        if not len(runner.crawlers) > 0:
            return {'finished': False, 'requests': None}
        crawler = list(runner.crawlers)[0]
        # get spider by crawler
        spider = crawler.spider
        # get start requests
        requests = list(spider.start_requests())
        if not requests and hasattr(spider, 'start'):
            requests = list(spider.start())
        requests = list(map(lambda r: process_request(r), requests))
        return {'finished': True, 'requests': requests}
    except:
        return {'finished': False, 'requests': None}
    finally:
        os.chdir(work_cwd)


if __name__ == '__main__':
    from munch import munchify
    
    args = {'logfile': None, 'loglevel': None, 'nolog': None, 'profile': None, 'pidfile': None, 'set': [], 'pdb': None,
            'spargs': {}, 'pipelines': None, 'nolinks': None, 'noitems': None, 'nocolour': None,
            'rules': None, 'callback': 'parse_detail', 'meta': None, 'depth': 1, 'verbose': None,
            'url': 'http://quotes.toscrape.com/author/Albert-Einstein'}
    
    args = munchify(args)
    
    project_path = '/Users/CQC/Gerapy/projects/ssss'
    get_follow_requests_and_items(project_path, 'quotes', args)
