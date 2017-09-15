import json
import logging

import pymongo
import time
from zhihusite.items import *
from azure.storage.blob import BlockBlobService
from azure.storage.table import TableService, Entity
import pymongo
from hashlib import md5
from azure.storage.blob import ContentSettings, PublicAccess


class BasePipeline(object):
    def process_item(self, item, spider):
        now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        if not item.get('crawled_at'):
            item['crawled_at'] = now
        return item


class QuestionPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, QuestionItem):
            item['created_at'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(item.get('created')))
            del item['created']
            item['type'] = item.get('question_type')
            del item['question_type']
            topics = item.get('topics')
            ts = []
            for topic in topics:
                ts.append({
                    'name': topic.get('name'),
                    'id': topic.get('id'),
                })
            item['topics'] = ts

            related = item.get('related')
            rt = []
            for r in related:
                rt.append({
                    'title': r.get('title'),
                    'id': r.get('id'),
                    'url': 'https://www.zhihu.com/question/' + str(r.get('id'))
                })
            item['related'] = rt

        return item
class ConversationPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, ConversationItem):
            conversation = item.get('conversation')
            dialogs = []
            for index, c in enumerate(conversation):
                dialog = {}
                if index % 2 == 0:
                    dialog['type'] = 'question'
                else:
                    dialog['type'] = 'answer'
                dialog['text'] = c['content']
                dialogs.append(dialog)
            item['conversation'] = dialogs
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ConversationItem):
            self.db[item.mongo_table_name].insert(dict(item))
        else:
            if not self.db[item.mongo_table_name].find_one({'id': item['id']}):
                self.db[item.mongo_table_name].insert(dict(item))
        return item


class AzureStorageTablePipeline(object):
    def __init__(self, azure_storage_account, azure_storage_key, azure_endpoint_suffix):
        self.azure_storage_account = azure_storage_account
        self.azure_storage_key = azure_storage_key
        self.azure_endpoint_suffix = azure_endpoint_suffix
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            azure_storage_account=crawler.settings.get('AZURE_STORAGE_ACCOUNT'),
            azure_storage_key=crawler.settings.get('AZURE_STORAGE_KEY'),
            azure_endpoint_suffix=crawler.settings.get('AZURE_ENDPOINT_SUFFIX')
        )

    def open_spider(self, spider):
        self.table_service = TableService(account_name=self.azure_storage_account, account_key=self.azure_storage_key,
                                          endpoint_suffix=self.azure_endpoint_suffix)
        if not self.table_service.exists(UserItem.table_name):
            self.table_service.create_table(UserItem.table_name)
        if not self.table_service.exists(QuestionItem.table_name):
            self.table_service.create_table(QuestionItem.table_name)
        if not self.table_service.exists(AnswerItem.table_name):
            self.table_service.create_table(AnswerItem.table_name)
        if not self.table_service.exists(ConversationItem.table_name):
            self.table_service.create_table(ConversationItem.table_name)

    def md5(self, text):
        m = md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()

    def process_item(self, item, spider):
        entity = Entity()
        entity.PartitionKey = item.partition_key
        if isinstance(item, ConversationItem):
            entity.RowKey = self.md5(json.dumps(item.get(item.row_key)))
        else:
            entity.RowKey = item.get(item.row_key)
        for field in item.fields:
            value = item.get(field)
            if isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            setattr(entity, field, value)
        self.logger.debug('Entity' + json.dumps(dict(entity)))
        self.table_service.insert_or_replace_entity(item.table_name, entity)
        return item