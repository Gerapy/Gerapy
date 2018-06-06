import pymysql
from twisted.internet.threads import deferToThread


class MySQLPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()
    
    def close_spider(self, spider):
        self.db.close()
    
    def _process_item(self, item, spider):
        allowed_spiders = item.mongodb_spiders
        allowed_tables = item.mongodb_tables
        if allowed_spiders and spider.name in allowed_spiders:
            for allowed_table in allowed_tables:
                data = dict(item)
                keys = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                sql = 'insert into %s (%s) values (%s)' % (allowed_table, keys, values)
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
        return item
    
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
