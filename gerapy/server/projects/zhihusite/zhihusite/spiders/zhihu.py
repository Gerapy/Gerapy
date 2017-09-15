# -*- coding: utf-8 -*-
import json

import logging
from scrapy import Spider, Request

from zhihusite.items import UserItem, QuestionItem, ConversationItem, AnswerItem
from zhihusite.proxy import WebProxyTool


class ZhihuSpider(Spider):
    name = 'zhihusite'
    allowed_domains = ['www.zhihu.com', 'api.zhihu.com', 'www.bing.com']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    start_users = ['jing-lei', 'lawrencelry', 'shen']
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    questions_url = 'https://www.zhihu.com/api/v4/members/{user}/answers?include={include}&offset={offset}&limit={limit}&sort_by=created'
    questions_query = 'data[*].is_normal,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'

    tiwen_url = 'https://www.zhihu.com/api/v4/members/{user}/questions?include=data[*].created,answer_count,follower_count,author&offset={offset}&limit={limit}'

    answers_url = 'https://www.zhihu.com/api/v4/questions/{question}/answers?include=data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics&offset={offset}&limit={limit}&sort_by=default'

    comments_url = 'https://www.zhihu.com/api/v4/answers/{answer}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit={limit}&offset={offset}&status=open'

    conversation_url = 'https://www.zhihu.com/api/v4/comments/{comment}/conversation?include=%24%5B*%5D.author%2Creply_to_author%2Ccontent'

    question_url = 'https://api.zhihu.com/questions/{id}'

    similar_questions_url = 'https://www.zhihu.com/api/v4/questions/{id}/similar-questions?include=data%5B*%5D.answer_count%2Cauthor&limit=10'

    api_headers = {
        'Authorization': 'Bearer gt2.0AAAAAAT_VnoLrgG8LgJAAAAAAAtNVQJgAgD_vvosPQabsVYX0w3tcIoFfKK7bQ==',
        'User-Agent': 'osee2unifiedRelease/3.52.0 (iPhone; iOS 10.3.1; Scale/3.00)',
        'x-app-za': 'OS=iOS&Release=10.3.1&Model=iPhone9,2&VersionName=3.52.0&VersionCode=622&Width=1242&Height=2208',
    }

    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    }

    logger = logging.getLogger(__name__)

    tool = WebProxyTool()

    # 优先级
    # parse_followers 1
    # parse_followees 1
    # parse_user 2
    # parse_questions 3
    # parse_question 4
    # parse_similar_question 5


    def start_requests(self):
        for start_user in self.start_users:
            origin_url = self.user_url.format(user=start_user, include=self.user_query)
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url, self.parse_user,
                          headers=self.custom_headers, meta={'origin': origin_url}, priority=2)

        for start_user in self.start_users:
            origin_url = self.follows_url.format(user=start_user, include=self.follows_query, limit=20, offset=0)
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_follows, headers=self.custom_headers, meta={'origin': origin_url}, priority=1)

            origin_url = self.followers_url.format(user=start_user, include=self.followers_query, limit=20, offset=0)
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_followers, headers=self.custom_headers, meta={'origin': origin_url}, priority=1)

            origin_url = self.questions_url.format(user=start_user, include=self.questions_query, limit=20, offset=0)
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_questions, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

            origin_url = self.tiwen_url.format(user=start_user, limit=20, offset=0)
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_tiwen, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

    def parse_user(self, response):
        result = json.loads(response.text)

        # 个人信息
        user_item = UserItem()

        for field in user_item.fields:
            if field in result.keys():
                user_item[field] = result.get(field)
        yield user_item

        # 关注
        origin_url = self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20,
                                             offset=0)

        self.logger.debug('Origin Url: ' + origin_url)

        url = self.tool.get_crawl_url(origin_url)

        yield Request(url,
                      self.parse_follows, headers=self.custom_headers, meta={'origin': origin_url}, priority=2)

        # 粉丝
        origin_url = self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20,
                                               offset=0)

        self.logger.debug('Origin Url: ' + origin_url)

        url = self.tool.get_crawl_url(origin_url)

        yield Request(
            url,
            self.parse_followers, headers=self.custom_headers, meta={'origin': origin_url}, priority=1)

        # 回答问题
        origin_url = self.questions_url.format(user=result.get('url_token'), include=self.questions_query, limit=20,
                                               offset=0)

        self.logger.debug('Origin Url: ' + origin_url)

        url = self.tool.get_crawl_url(origin_url)

        yield Request(url,
                      self.parse_questions, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

        # 提问问题
        origin_url = self.tiwen_url.format(user=result.get('url_token'), limit=20,
                                           offset=0)

        self.logger.debug('Origin Url: ' + origin_url)

        url = self.tool.get_crawl_url(origin_url)

        yield Request(url,
                      self.parse_tiwen, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

    def parse_questions(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                if 'question' in result.keys():
                    question = result.get('question')

                    # 问题详情

                    origin_url = self.question_url.format(id=question.get('id'))

                    self.logger.debug('Origin Url: ' + origin_url)

                    url = self.tool.get_crawl_url(origin_url)

                    yield Request(url, self.parse_question, headers=self.api_headers, meta={'origin': origin_url},
                                  priority=4)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')

            # 下一页
            origin_url = next_page

            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_questions, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

    def parse_tiwen(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                if 'id' in result.keys():
                    id = result.get('id')

                    # 问题详情

                    origin_url = self.question_url.format(id=id)

                    self.logger.debug('Origin Url: ' + origin_url)

                    url = self.tool.get_crawl_url(origin_url)

                    yield Request(url, self.parse_question, headers=self.api_headers, meta={'origin': origin_url},
                                  priority=4)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')

            # 下一页
            origin_url = next_page

            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_tiwen, headers=self.custom_headers, meta={'origin': origin_url}, priority=3)

    def parse_question(self, response):

        if response.text:
            result = json.loads(response.text)
            question_item = QuestionItem()
            for field in question_item.fields:
                question_item[field] = result.get(field)

            origin_url = self.similar_questions_url.format(id=result.get('id'))
            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url, callback=self.parse_similar_questions,
                          headers=self.custom_headers, meta={'question': question_item, 'origin': origin_url},
                          priority=5)

            # origin_url = self.answers_url.format(question=result.get('id'), offset=0, limit=20)
            # self.logger.debug('Origin Url: ' + origin_url)
            #
            # url = self.tool.get_crawl_url(origin_url)
            #
            # yield Request(url=url, callback=self.parse_answers, headers=self.custom_headers, priority=6)

    def parse_similar_questions(self, response):
        if response.text:
            result = json.loads(response.text)
            question_item = response.meta.get('question')
            question_item['related'] = result.get('data')

            if result.get('data'):
                for question in result.get('data'):
                    origin_url = self.question_url.format(id=question.get('id'))

                    self.logger.debug('Similar Question Origin Url: ' + origin_url)

                    url = self.tool.get_crawl_url(origin_url)

                    yield Request(url, self.parse_question, headers=self.api_headers, meta={'origin': origin_url},
                                  priority=4)

            yield question_item

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                # 用户
                origin_url = self.user_url.format(user=result.get('url_token'), include=self.user_query)

                self.logger.debug('Origin Url: ' + origin_url)

                url = self.tool.get_crawl_url(origin_url)

                yield Request(url,
                              self.parse_user, headers=self.custom_headers, meta={'origin': origin_url}, priority=2)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')

            # 下一页
            origin_url = next_page

            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_follows, headers=self.custom_headers, meta={'origin': origin_url}, priority=1)

    def parse_followers(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                # 用户
                origin_url = self.user_url.format(user=result.get('url_token'), include=self.user_query)

                self.logger.debug('Origin Url: ' + origin_url)

                url = self.tool.get_crawl_url(origin_url)

                yield Request(url,
                              self.parse_user, headers=self.custom_headers, meta={'origin': origin_url}, priority=2)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')

            # 下一页
            origin_url = next_page

            self.logger.debug('Origin Url: ' + origin_url)

            url = self.tool.get_crawl_url(origin_url)

            yield Request(url,
                          self.parse_followers, headers=self.custom_headers, meta={'origin': origin_url}, priority=1)

    def parse_answers(self, response):
        if response.text:

            results = json.loads(response.text)

            if 'data' in results.keys():
                for result in results.get('data'):
                    item = AnswerItem()

                    for field in item.fields:
                        if field in result.keys():
                            item[field] = result.get(field)

                    item['author'] = result.get('author').get('url_token')
                    item['question'] = result.get('question').get('id')
                    yield item
                    origin_url = self.comments_url.format(answer=result.get('id'), offset=0, limit=20)
                    self.logger.debug('Origin Url: ' + origin_url)

                    url = self.tool.get_crawl_url(origin_url)

                    yield Request(url,
                                  self.parse_comments, headers=self.custom_headers,
                                  meta={'answer': result.get('id'), 'origin': origin_url},
                                  priority=7)

            if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
                next_page = results.get('paging').get('next')
                origin_url = next_page
                self.logger.debug('Origin Url: ' + origin_url)

                url = self.tool.get_crawl_url(origin_url)

                yield Request(url,
                              self.parse_answers, headers=self.custom_headers, priority=6, meta={'origin': origin_url})

    def parse_comments(self, response):
        if response.text:
            results = json.loads(response.text)

            if 'data' in results.keys():
                for result in results.get('data'):
                    if result.get('reply_to_author'):
                        origin_url = self.conversation_url.format(comment=result.get('id'))
                        self.logger.debug('Origin Url: ' + origin_url)

                        url = self.tool.get_crawl_url(origin_url)

                        yield Request(url=url, callback=self.parse_conversation,
                                      headers=self.custom_headers,
                                      meta={'answer': response.meta.get('answer'), 'origin': origin_url},
                                      priority=8)

            if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
                next_page = results.get('paging').get('next')
                origin_url = next_page
                self.logger.debug('Origin Url: ' + origin_url)

                url = self.tool.get_crawl_url(origin_url)

                yield Request(url,
                              self.parse_comments, headers=self.custom_headers,
                              meta={'answer': response.meta.get('answer'), 'origin': origin_url}, priority=7)

    def parse_conversation(self, response):
        if response.text:
            results = json.loads(response.text)
            conversation_item = ConversationItem()
            conversation_item['answer'] = response.meta.get('answer')
            conversation_item['conversation'] = results
            yield conversation_item
