import pymongo
from twisted.internet.threads import deferToThread


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_database):
        self.mongo_uri = mongo_uri
        self.mongo_database = mongo_database
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_database=crawler.settings.get('MONGO_DATABASE')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.database = self.client[self.mongo_database]
    
    def _process_item(self, item, spider):
        allowed_spiders = item.get('mongodb_spiders')
        allowed_collections = item.get('mongodb_collections')
        if allowed_spiders and spider in allowed_spiders:
            for allowed_collection in allowed_collections:
                self.database[allowed_collection].insert(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)