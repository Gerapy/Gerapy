import json
import logging
import os
import sys
import optparse
from scrapy.commands import ScrapyCommand as BaseParser
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.settings.deprecated import check_deprecated_settings
from w3lib.url import is_url
from scrapy.utils.conf import arglist_to_dict
from scrapy.exceptions import UsageError
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.utils import display
from scrapy.utils.spider import iterate_spider_output, spidercls_for_request
import multiprocessing
from twisted.internet import reactor

from gerapy.server.core.utils import process_request, process_response, process_item

logger = logging.getLogger(__name__)

dfs = set()

FATAL_ERROR = -100


class SpiderParser(BaseParser):
    requires_project = True
    spider = None
    items = {}
    requests = {}
    first_response = None
    
    def short_desc(self):
        """
        short description
        :return: string
        """
        return "Parse URL (using its spider) and print the results"
    
    def add_options(self, parser):
        """
        option parser
        :param parser: 
        :return: 
        """
        BaseParser.add_options(self, parser)
        parser.add_option("--spider", dest="spider", default=None,
                          help="use this spider without looking for one")
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("--pipelines", action="store_true",
                          help="process items through pipelines")
        parser.add_option("--nolinks", dest="nolinks", action="store_true",
                          help="don't show links to follow (extracted requests)")
        parser.add_option("--noitems", dest="noitems", action="store_true",
                          help="don't show scraped items")
        parser.add_option("--nocolour", dest="nocolour", action="store_true",
                          help="avoid using pygments to colorize the output")
        parser.add_option("-r", "--rules", dest="rules", action="store_true",
                          help="use CrawlSpider rules to discover the callback")
        parser.add_option("-c", "--callback", dest="callback",
                          help="use this callback for parsing, instead looking for a callback")
        parser.add_option("-m", "--meta", dest="meta",
                          help="inject extra meta into the Request, it must be a valid raw json string")
        parser.add_option("-d", "--depth", dest="depth", type="int", default=1,
                          help="maximum depth for parsing requests [default: %default]")
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                          help="print each depth level one by one")
    
    @property
    def max_level(self):
        """
        get max level
        :return: max level
        """
        levels = list(self.items.keys()) + list(self.requests.keys())
        if not levels:
            return 0
        return max(levels)
    
    def add_items(self, lvl, new_items):
        """
        add items to self.items
        :param lvl: levels
        :param new_items: new items
        :return: None
        """
        old_items = self.items.get(lvl, [])
        self.items[lvl] = old_items + new_items
    
    def add_requests(self, lvl, new_reqs):
        """
        add requests
        :param lvl: level
        :param new_reqs: new requests
        :return: 
        """
        old_reqs = self.requests.get(lvl, [])
        self.requests[lvl] = old_reqs + new_reqs
    
    def print_items(self, lvl=None, colour=True):
        """
        print items by pprint
        :param lvl: level
        :param colour: color
        :return: None
        """
        if lvl is None:
            items = [item for lst in self.items.values() for item in lst]
        else:
            items = self.items.get(lvl, [])
        
        print("# Scraped Items ", "-" * 60)
        display.pprint([dict(x) for x in items], colorize=colour)
    
    def print_requests(self, lvl=None, colour=True):
        """
        print requests by pprint
        :param lvl: level
        :param colour: color
        :return: None
        """
        if lvl is None:
            levels = list(self.requests.keys())
            if levels:
                requests = self.requests[max(levels)]
            else:
                requests = []
        else:
            requests = self.requests.get(lvl, [])
        
        print("# Requests ", "-" * 65)
        display.pprint(requests, colorize=colour)
    
    def print_results(self, opts):
        """
        print results including items and requests
        :param opts: options
        :return: None
        """
        colour = not opts.nocolour
        if opts.verbose:
            for level in range(1, self.max_level + 1):
                print('\n>>> DEPTH LEVEL: %s <<<' % level)
                if not opts.noitems:
                    self.print_items(level, colour)
                if not opts.nolinks:
                    self.print_requests(level, colour)
        else:
            print('\n>>> STATUS DEPTH LEVEL %s <<<' % self.max_level)
            if not opts.noitems:
                self.print_items(colour=colour)
            if not opts.nolinks:
                self.print_requests(colour=colour)
    
    def get_items(self, lvl=None):
        """
        return items
        :param lvl: level
        :return: items
        """
        if lvl is None:
            items = [item for lst in self.items.values() for item in lst]
        else:
            items = self.items.get(lvl, [])
        items_array = []
        for item in items:
            items_array.append(process_item(item))
        return items_array
    
    def get_requests(self, lvl=None):
        """
        get requests
        :param lvl: level
        :return: requests
        """
        if lvl is None:
            levels = list(self.requests.keys())
            if levels:
                requests = self.requests[max(levels)]
            else:
                requests = []
        else:
            requests = self.requests.get(lvl, [])
        
        requests_array = []
        for request in requests:
            print('Request', request, self.get_callback(request))
            requests_array.append(process_request(request))
        
        return requests_array
    
    def get_response(self):
        return process_response(self.first_response)
    
    def get_results(self, opts):
        results = []
        
        for level in range(1, self.max_level + 1):
            if not opts.noitems:
                items = self.get_items(level)
                results += items
            if not opts.nolinks:
                requests = self.get_requests(level)
                results += requests
        return results
    
    def run_callback(self, response, cb):
        items, requests = [], []
        for x in iterate_spider_output(cb(response)):
            if isinstance(x, (BaseItem, dict)):
                items.append(x)
            elif isinstance(x, Request):
                requests.append(x)
        return items, requests
    
    def get_callback(self, request):
        if getattr(self.spidercls, 'rules', None):
            rule_index = request.meta.get('rule', -1)
            if rule_index >= 0 and rule_index < len(self.spidercls.rules):
                rule = self.spidercls.rules[rule_index]
                return rule.callback or 'parse'
            elif request.callback:
                return request.callback.__name__
    
    def get_callback_from_rules(self, spider, response):
        if getattr(spider, 'rules', None):
            for rule in spider.rules:
                if rule.link_extractor.matches(response.url):
                    return rule.callback or "parse"
        else:
            logger.error('No CrawlSpider rules found in spider %(spider)r, '
                         'please specify a callback to use for parsing',
                         {'spider': spider.name})
    
    def set_spidercls(self, url, opts):
        spider_loader = self.crawler_process.spider_loader
        if opts.spider:
            try:
                self.spidercls = spider_loader.load(opts.spider)
            except KeyError:
                logger.error('Unable to find spider: %(spider)s',
                             {'spider': opts.spider})
        else:
            self.spidercls = spidercls_for_request(spider_loader, Request(url))
            if not self.spidercls:
                logger.error('Unable to find spider for: %(url)s',
                             {'url': url})
        
        # Request requires callback argument as callable or None, not string
        request = Request(url, None)
        _start_requests = lambda s: [self.prepare_request(s, request, opts)]
        self.spidercls.start_requests = _start_requests
    
    def start_parsing(self, url, opts):
        print('Spidercls', self.spidercls)
        print('Opt', opts.spargs)
        
        self.crawler_process.crawl(self.spidercls, **opts.spargs)
        print('Crawwwwwlers', self.crawler_process, self.crawler_process.crawlers)
        if not len(self.crawler_process.crawlers) > 0:
            return FATAL_ERROR
        self.pcrawler = list(self.crawler_process.crawlers)[0]
        # self.crawler_process.start()
        # self.crawler_process.start()
        d = self.crawler_process.join()
        d.addBoth(lambda _: reactor.stop())
        
        reactor.run()
        
        if not self.first_response:
            logger.error('No response downloaded for: %(url)s',
                         {'url': url})
    
    def prepare_request(self, spider, request, opts):
        def callback(response):
            # memorize first request
            if not self.first_response:
                self.first_response = response
            
            # determine real callback
            cb = response.meta['_callback']
            if not cb:
                if opts.callback:
                    cb = opts.callback
                elif opts.rules and self.first_response == response:
                    cb = self.get_callback_from_rules(spider, response)
                    
                    if not cb:
                        logger.error('Cannot find a rule that matches %(url)r in spider: %(spider)s',
                                     {'url': response.url, 'spider': spider.name})
                        return
                else:
                    cb = 'parse'
            
            if not callable(cb):
                cb_method = getattr(spider, cb, None)
                if callable(cb_method):
                    cb = cb_method
                else:
                    logger.error('Cannot find callback %(callback)r in spider: %(spider)s',
                                 {'callback': cb, 'spider': spider.name})
                    return
            
            # parse items and requests
            depth = response.meta['_depth']
            
            items, requests = self.run_callback(response, cb)
            if opts.pipelines:
                itemproc = self.pcrawler.engine.scraper.itemproc
                for item in items:
                    itemproc.process_item(item, spider)
            
            # process request callback
            for request in requests:
                request.callback = self.get_callback(request)
            
            self.add_items(depth, items)
            self.add_requests(depth, requests)
            
            if depth < opts.depth:
                for req in requests:
                    req.meta['_depth'] = depth + 1
                    req.meta['_callback'] = req.callback
                    req.callback = callback
                return requests
        
        # update request meta if any extra meta was passed through the --meta/-m opts.
        if opts.meta:
            request.meta.update(opts.meta)
        
        request.meta['_depth'] = 1
        request.meta['_callback'] = request.callback
        request.callback = callback
        return request
    
    def process_options(self, args, opts):
        BaseParser.process_options(self, args, opts)
        
        self.process_spider_arguments(opts)
        self.process_request_meta(opts)
    
    def process_spider_arguments(self, opts):
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
    
    def process_request_meta(self, opts):
        if opts.meta:
            try:
                opts.meta = json.loads(opts.meta)
            except ValueError:
                raise UsageError("Invalid -m/--meta value, pass a valid json string to -m or --meta. " \
                                 "Example: --meta='{\"foo\" : \"bar\"}'", print_help=False)
    
    def run(self, args, opts):
        # parse arguments
        if not len(args) == 1 or not is_url(args[0]):
            raise UsageError()
        else:
            url = args[0]
        
        # prepare spidercls
        self.set_spidercls(url, opts)
        
        if self.spidercls and opts.depth > 0:
            start_status = self.start_parsing(url, opts)
            if start_status == FATAL_ERROR:
                return start_status
            self.print_results(opts)
            results = self.get_results(opts)
            print(len(results))
            return results


def execute(url, project_path, spider_name, callback, result, *arg, **kwargs):
    """
    execute parsing
    :param url: url
    :param project_path: project path
    :param spider_name: spider name
    :param callback: callback
    :param result: results generated by multiprocessing
    :return: 
    """
    argv = sys.argv
    argv.append(url)
    if spider_name:
        argv.append('--spider')
        argv.append(spider_name)
    if callback:
        argv.append('--callback')
        argv.append(callback)
    
    work_cwd = os.getcwd()
    print('Word cwd', work_cwd)
    try:
        # change work dir
        os.chdir(project_path)
        print('Move to ', project_path)
        # get settings of project
        settings = get_project_settings()
        print('Settings', settings)
        check_deprecated_settings(settings)
        # get args by optparse
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')
        # init SpiderParser
        spider_parser = SpiderParser()
        settings.setdict(spider_parser.default_settings, priority='command')
        spider_parser.settings = settings
        spider_parser.add_options(parser)
        opts, _ = parser.parse_args(args=argv[1:])
        args = [url]
        spider_parser.process_options(args, opts)
        # use CrawlerRunner instead of CrawlerProcess
        spider_parser.crawler_process = CrawlerRunner(settings)
        print(spider_parser.crawler_process)
        # spider_parser.crawler_process = CrawlerProcess(settings)
        status = spider_parser.run(args, opts)
        if status == FATAL_ERROR:
            result['requests'], result['items'], result['response'] = (None, None, None)
            result['finished'] = False
        else:
            # get follow requests, items, response
            requests, items, response = spider_parser.get_requests(), spider_parser.get_items(), spider_parser.get_response()
            result['requests'] = requests
            result['items'] = items
            result['response'] = response
            result['finished'] = True
    finally:
        print('Move out', work_cwd)
        os.chdir(work_cwd)


def get_follow_results(url, project_path, spider_name, callback):
    """
    run parser, get follow results by multiprocessing.Process
    :param url: url
    :param project: project
    :param spider: spider
    :param callback: callback
    :return: dict results
    """
    print('URL', url, 'pj', project_path)
    print('CWD', os.getcwd())
    try:
        manager = multiprocessing.Manager()
        result = manager.dict()
        jobs = []
        # use Process in case of reactor stop exception
        p = multiprocessing.Process(target=execute, args=(url, project_path, spider_name, callback, result))
        jobs.append(p)
        p.start()
        # processes
        for proc in jobs:
            proc.join()
        print('Result', result)
        return dict(result)
    except Exception as e:
        print(e.args)
        return {'finished': False}


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
    url = 'http://tech.china.com/article/20180511/20180511136031.html'
    spider_name = 'quotes'
    # callback = None
    project_path = '/Users/CQC/Gerapy/projects/ssss'
    # result = get_follow_results(url, project_path, spider_name, callback)
    # print('Result', result)
    requests = get_start_requests(project_path, spider_name)
    print(requests)
    
    url = 'http://quotes.toscrape.com/author/Albert-Einstein'
    callback = 'parse_detail'
    result = get_follow_results(url, project_path, spider_name, callback)
