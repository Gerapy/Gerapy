import logging
import requests


class ProxyMiddleware():
    def __init__(self, proxy_url, proxy_fail_times):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        self.proxy_fail_times = proxy_fail_times
    
    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False
    
    def process_request(self, request, spider):
        if request.meta.get('retry_times') >= self.proxy_fail_times:
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('Using Proxy {proxy}'.format(proxy=proxy))
                request.meta['proxy'] = uri
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL'),
            proxy_fail_times=settings.get('PROXY_FAIL_TIMES', 1),
        )
