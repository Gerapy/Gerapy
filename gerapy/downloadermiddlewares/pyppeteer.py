from scrapy.http import HtmlResponse
from logging import getLogger
import asyncio
import pyppeteer


class PyppeteerMiddleware():
    def __init__(self, **args):
        self.logger = getLogger(__name__)
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(
            pyppeteer.launch(headless=True, args=['--no-sandbox']))
        self.args = args
    
    def render(self, url, retries=8, script=None, wait=0.2, scrolldown=False, sleep=0,
               timeout=8.0, keep_page=True, with_result=False):
        """
        render page with pyppeteer
        :param url: page url
        :param retries: max retry times
        :param script: js script to evaluate
        :param wait: number of seconds to wait before loading the page, preventing timeouts
        :param scrolldown: how many times to page down
        :param sleep: how many long to sleep after initial render
        :param timeout: the longest wait time, otherwise raise timeout error
        :param keep_page: keep page not to be closed, browser object needed
        :param browser: pyppetter browser object
        :param with_result: return with js evaluation result
        :return: content, [result]
        """
        # define async render
        async def async_render(url, script, scrolldown, sleep, wait, timeout, keep_page):
            try:
                # basic render
                page = await self.browser.newPage()
                await asyncio.sleep(wait)
                await page.goto(url, options={'timeout': int(timeout * 1000)})
                
                result = None
                # evaluate with script
                if script:
                    result = await page.evaluate(script)
                
                # scroll down for {scrolldown} times
                if scrolldown:
                    for _ in range(scrolldown):
                        await page._keyboard.down('PageDown')
                        await asyncio.sleep(sleep)
                else:
                    await asyncio.sleep(sleep)
                if scrolldown:
                    await page._keyboard.up('PageDown')
                
                # get html of page
                content = await page.content()
                
                # if keep page, do not close it
                if not keep_page:
                    await page.close()
                
                return content, result
            except TimeoutError:
                return None
        
        content, result = None, None
        # retry for {retries} times
        for i in range(retries):
            if not content:
                content, result = self.loop.run_until_complete(
                    async_render(url=url, script=script, sleep=sleep, wait=wait,
                                 scrolldown=scrolldown, timeout=timeout, keep_page=keep_page))
            else:
                break
        
        # if need to return js evaluation result
        if with_result:
            return content, result
        return content
    
    def process_request(self, request, spider):
        """
        :param request: request object
        :param spider: spider object
        :return: HtmlResponse
        """
        self.logger.debug('Render %s', request.url)
        try:
            html = self.render(request.url)
            return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8',
                                status=200)
        except pyppeteer.errors.TimeoutError:
            return HtmlResponse(url=request.url, status=500, request=request)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(**crawler.settings.get('PYPPETEER_ARGS'))
