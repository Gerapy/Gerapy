# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class UserItem(Item):
    table_name = 'zhihuusers'

    mongo_table_name = 'users'

    partition_key = 'user'

    row_key = 'id'

    id = Field()
    name = Field()
    avatar_url = Field()
    headline = Field()
    description = Field()
    url = Field()
    url_token = Field()
    gender = Field()
    cover_url = Field()
    type = Field()
    badge = Field()

    answer_count = Field()
    articles_count = Field()
    commercial_question_count = Field()
    favorite_count = Field()
    favorited_count = Field()
    follower_count = Field()
    following_columns_count = Field()
    following_count = Field()
    pins_count = Field()
    question_count = Field()
    thank_from_count = Field()
    thank_to_count = Field()
    thanked_count = Field()
    vote_from_count = Field()
    vote_to_count = Field()
    voteup_count = Field()
    following_favlists_count = Field()
    following_question_count = Field()
    following_topic_count = Field()
    marked_answers_count = Field()
    mutual_followees_count = Field()
    hosted_live_count = Field()
    participated_live_count = Field()

    locations = Field()
    educations = Field()
    employments = Field()


    crawled_at = Field()



class QuestionItem(Item):
    table_name = 'zhihuquestions'

    mongo_table_name = 'questions'

    partition_key = 'question'

    row_key = 'id'

    topics = Field()
    detail = Field()
    answer_count = Field()
    id = Field()
    url = Field()
    created = Field()
    created_at = Field()
    type = Field()
    question_type = Field()
    follower_count = Field()
    title = Field()
    related = Field()
    crawled_at = Field()


class AnswerItem(Item):
    table_name = 'zhihuanswers'

    mongo_table_name = 'answers'

    partition_key = 'answer'

    row_key = 'id'

    id = Field()
    content = Field()
    url = Field()
    created = Field()
    author = Field()
    question = Field()
    comment_count = Field()
    voteup_count = Field()
    thumbnail = Field()
    crawled_at = Field()


class ConversationItem(Item):
    table_name = 'zhihuconversations'

    partition_key = 'conversation'

    mongo_table_name = 'conversations'

    row_key = 'conversation'

    answer = Field()

    conversation = Field()
    crawled_at = Field()