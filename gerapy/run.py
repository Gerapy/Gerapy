import inspect

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

data = {"spiders": [{"name": "china", "attrs": [{"key": "http_user", "value": "admin"}, {"key": "http_pass", "value": "admin"}], "extractors": [{"callback": "parse_item", "item": "NewsItem", "attrs": {"title": [{"method": "xpath", "arg": "//h1[@id=\"chan_newsTitle\"]/text()", "processor": "Compose(TakeFirst(), lambda s: s.strip())"}], "content": [{"method": "xpath", "arg": "//div[@id=\"chan_newsDetail\"]//text()", "processor": "Compose(Join(), lambda s: s.strip())"}], "url": [{"method": "attr", "arg": "url"}], "publish_time": [{"method": "xpath", "arg": "//div[@id=\"chan_newsInfo\"]/text()", "re": "(\\d+-\\d+-\\d+\\s\\d+:\\d+:\\d+)"}], "source": [{"method": "xpath", "arg": "//div[@id=\"chan_newsInfo\"]/text()", "re": "\u6765\u6e90\uff1a(.*)", "processor": "Compose(Join(), lambda s: s.strip())"}], "website": [{"method": "value", "arg": "\u4e2d\u534e\u7f51"}]}}], "rules": [{"allow": ["article\\/.*\\.html"], "restrict_xpaths": ["//div[@id=\"pageStyle\"]//a[contains(., \"\u4e0b\u4e00\u9875\")]"], "callback": "parse_item", "follow": False}, {"restrict_xpaths": ["//div[@id=\"pageStyle\"]//a[contains(., \"\u4e0b\u4e00\u9875\")]"]}, {}], "startUrls": {"list": ["http://tech.china.com/articles/"], "mode": "list"}, "allowedDomains": ["tech.china.com"], "code": "", "customSettings": "{\n\"SPLASH_URL\": \"tecent.cuiqingcai.com:8050\"\n}"}], "items": [{"name": "NewsItem", "attrs": {"title": {"outProcessor": ""}, "content": {"outProcessor": ""}, "source": {"outProcessor": ""}, "url": {}, "website": {"outProcessor": ""}, "crawl_time": {"outProcessor": ""}, "publish_time": {}, "table": {"value": "news"}, "collection": {"value": "news"}}}]}

from jinja2 import Template

template = Template(open('templates/spiders/crawl.tmpl').read())
for spider in data.get('spiders'):
    r = template.render(spider=spider)
    print('R', r)
