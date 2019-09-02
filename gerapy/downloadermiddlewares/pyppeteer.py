import websockets
from scrapy.http import HtmlResponse
import asyncio
import pyppeteer
import logging
from concurrent.futures._base import TimeoutError
from gerapy import get_logger

pyppeteer_level = logging.WARNING
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)

logger = get_logger(__name__)


class PyppeteerMiddleware():
    def __init__(self, **args):
        """
        init logger, loop, browser
        :param args:
        """
        self.args = args
        self.loop = asyncio.get_event_loop()
    
    def __del__(self):
        """
        close loop
        :return:
        """
        self.loop.close()
    
    def render(self, url, retries=1, script=None, wait=0.3, scrolldown=False, sleep=0,
               timeout=8.0, keep_page=False):
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
        browser = self.loop.run_until_complete(pyppeteer.launch(headless=True,
                                                                handleSIGTERM=False,
                                                                handleSIGINT=False))
        
        # define async render
        async def async_render(url, script, scrolldown, sleep, wait, timeout, keep_page):
            try:
                # basic render
                page = await browser.newPage()
                await asyncio.sleep(wait)
                response = await page.goto(url, options={'timeout': int(timeout * 1000)})
                if response.status != 200:
                    return None, None, response.status
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
                
                return content, result, response.status
            except TimeoutError:
                return None, None, 500
            finally:
                # if keep page, do not close it
                if not keep_page:
                    await page.close()
        
        content, result, status = [None] * 3
        
        # retry for {retries} times
        for i in range(retries):
            if not content:
                content, result, status = self.loop.run_until_complete(
                    async_render(url=url, script=script, sleep=sleep, wait=wait,
                                 scrolldown=scrolldown, timeout=timeout, keep_page=keep_page))
            else:
                break
        self.loop.run_until_complete(browser.close())
        # if need to return js evaluation result
        return content, result, status
    
    def process_request(self, request, spider):
        """
        :param request: request object
        :param spider: spider object
        :return: HtmlResponse
        """
        if request.meta.get('render'):
            try:
                html, result, status = self.render(request.url, **self.args)
                return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8',
                                    status=status)
            except websockets.exceptions.ConnectionClosed:
                pass
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(**crawler.settings.get('PYPPETEER_ARGS', {}))
