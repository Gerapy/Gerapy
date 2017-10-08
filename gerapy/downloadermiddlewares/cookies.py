import logging
import requests
import json


class CookiesMiddleware():
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url
    
    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False
    
    def process_request(self, request, spider):
        self.logger.debug('Getting Cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('Using Cookies {cookies}'.format(cookies=json.dumps(cookies)))
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )
