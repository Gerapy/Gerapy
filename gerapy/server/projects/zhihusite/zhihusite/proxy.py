from urllib.parse import quote
from Crypto.Cipher import AES
import base64

KEY = [222, 237, 16, 66, 28, 26, 85, 99, 114, 184, 88, 192, 37, 112, 222, 209, 241, 24, 175, 144, 173, 53, 105, 29, 24,
       26, 17, 218, 131, 236, 53, 209]
VECTOR = [146, 44, 101, 111, 66, 32, 99, 119, 231, 121, 211, 88, 77, 32, 104, 156]


class WebProxyTool():
    def __init__(self):
        self.padding = '\0'
        self.bs = 16
        self.pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        self.key = bytes(KEY)
        self.vector = bytes(VECTOR)

    def encrypt(self, decrypted_text):
        generator = AES.new(self.key, AES.MODE_CBC, self.vector)
        encrypted_text = generator.encrypt(self.pad(decrypted_text))
        result = base64.b64encode(encrypted_text)
        return result

    def decrypt(self, encrypted_text):
        content = base64.b64decode(encrypted_text)
        generator = AES.new(self.key, AES.MODE_CBC, self.vector)
        recovery = generator.decrypt(content)
        return recovery.rstrip(self.padding.encode('utf-8'))

    def get_crawl_url(self, url):
        format = 'http://www.bing.com/dict/proxy/proxy?k={k}'
        k = self.encrypt(url)
        return format.format(k=quote(self.encrypt(url).decode('utf-8')))

    def get_raw_url(self, url):
        url = url.replace('http://www.bing.com/dict/proxy/proxy?k=', '')
        print(url)
        result = self.decrypt(url)
        print(result)


if __name__ == '__main__':
    tool = WebProxyTool()
    url = 'http://www.bing.com/dict/proxy/proxy?k=%2BmYQzG09tUhSTo/6ttGI0m0L9o9MDVDXr8wERd2V3xaWPu/pH2BMyX%2B%2B2%2BxLZCceEbJhWI1ZEK2FduoAdm%2BvlditWrHrvWPm%2Bk15TziTOzPk%2B0NSNCHmXnFNnrgD59SullCal1KE7232eM9/Stc43aKfZ6eHV71/bBHaFPQxlLdnKz7509LKRtEQ4m9dDkh7DX1KPnW40ETeckS687mduFK4PF%2B17rJC7zjVB7EtMei7Z%2BXdDFtY7SLt6hK0/xOhuR7yykwJCOP1%2BbfOD1ZWcXudorMvCJ8490/d%2BIQjYB6NNseSpcHl2ANii2u%2BE8uLcjjZq5wOAL%2Bsv32mB1NgVIZTsdfmFy/5O7Lj8JMoBYmeZi9H8kT9jK3tS%2BvabZMQlb6Ilar83v3d4vLlSJoyURlPE2u%2BMXglVoT%2BvxLW/VsmlHUq9pZbhZC6THYW0LRtM144Fu99EKkIh2RtGPBSm6QEGXjFEJB5A0MBbCM4q0QM6hqXiufJqMCTPW8UDs9APzlrHAXINhbmqasdPxYa9Pkc7wx0exvbQ%2BVZhaz%2B3kWbeZyPmeDtaj7XP5zJFW%2BA'
    tool.get_raw_url(url)
