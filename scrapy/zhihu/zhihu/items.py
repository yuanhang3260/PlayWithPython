# -*- coding: utf-8 -*-
import scrapy


class AnswerItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  answer_id = scrapy.Field()
  content = scrapy.Field()
  imgs = scrapy.Field()


class QuestionAnswerItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  question_id = scrapy.Field()
  answer_id = scrapy.Field()
  content = scrapy.Field()
  imgs = scrapy.Field()
