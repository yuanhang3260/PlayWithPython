# -*- coding: utf-8 -*-
import json
import scrapy

from scrapy.selector import Selector
from zhihu.items import AnswerItem

class AnswerSpider(scrapy.Spider):
  name = 'answer_spider'
  allowed_domains = ['www.zhihu.com']
  start_urls = ['https://www.zhihu.com/']

  HEADERS = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/64.0.3282.140 '
                   'Safari/537.36')
  }

  QUESTION_ID = 34243513

  def parse(self, response):
    pass

  def start_requests(self):
    return [
      scrapy.Request(
        url = 'https://www.zhihu.com/question/%d' % self.QUESTION_ID,
        headers = self.HEADERS,
        callback = self.initial_analyze,
      ),
    ]

  def initial_analyze(self, response):
    answers = response.xpath('//div[@class="List-header"]//span/text()').extract_first()
    answers = int(answers.replace(',', ''))
    print "answers: %d" % answers

    get_answers_url = ('https://www.zhihu.com/api/v4/questions/%d/'
                       'answers?include=data[*].is_normal,admin_closed_comment,'
                       'reward_info,is_collapsed,annotation_action,'
                       'annotation_detail,collapse_reason,is_sticky,'
                       'collapsed_by,suggest_edit,comment_count,can_comment,'
                       'content,editable_content,voteup_count,'
                       'reshipment_settings,comment_permission,created_time,'
                       'updated_time,review_info,relevant_info,question,'
                       'excerpt,relationship.is_authorized,is_author,voting,'
                       'is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*]'
                       '.author.follower_count,badge[*].topics'
                       '&limit=%d&offset=0&sort_by=default') % (self.QUESTION_ID, 20)

    yield scrapy.Request(
      url = get_answers_url,
      headers = self.HEADERS,
      callback = self.extract_answers,
    )

  def extract_answers(self, response):
    resp = json.loads(response.text)
    
    if not resp:
      return

    for answer in resp['data']:
      item = AnswerItem()
      item['answer_id'] = answer['id']
      item['content'] = answer['content']

      content_selector = Selector(text=answer['content'])
      imgs = content_selector.xpath(
          '//figure//img[@class="origin_image zh-lightbox-thumb lazy"]/@data-original')
      item['imgs'] = imgs.extract()

      yield item

    # if not resp['paging']['is_end']:
    #   yield scrapy.Request(
    #     url = resp['paging']['next'],
    #     headers = self.HEADERS,
    #     callback = self.extract_answers,
    #   )
