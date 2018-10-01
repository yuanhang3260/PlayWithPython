# -*- coding: utf-8 -*-
import json
import re
import scrapy

from scrapy.selector import Selector
from urlparse import urljoin

from zhihu.items import QuestionAnswerItem

class FuliPicSpider(scrapy.Spider):
  name = 'fulipic_spider'
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

  COLLECTION_ID = 63441101
  START_URL = 'https://www.zhihu.com/collection/%d?page=1' % COLLECTION_ID

  def start_requests(self):
    return [
      scrapy.Request(
        url = self.START_URL,
        headers = self.HEADERS,
        callback = self.parse,
      ),
    ]

  def parse(self, response):
    answers = response.xpath('//*[@id="zh-list-collection-wrap"]'
                             '//div[@class="zm-item"]'
                             '//div[@class="zm-item-fav"]')

    for answer in answers:
      link = answer.xpath('.//link[@itemprop="url"]/@href').extract_first()
      match = re.match(r'/question/(\d+)/answer/(\d+)', link)
      question_id = match.group(1)
      answer_id = match.group(2)

      content = answer.xpath(
        './/div[@class="zm-item-rich-text expandable js-collapse-body"]'
        '//textarea[@class="content"]/text()').extract_first()
      content_selector = Selector(text=content)
      imgs = content_selector.xpath(
        './/figure/img[@class="origin_image zh-lightbox-thumb" or @class="content_image"]/@src')

      item = QuestionAnswerItem()
      item['question_id'] = int(question_id)
      item['answer_id'] = int(answer_id)
      item['content'] = content
      item['imgs'] = imgs.extract()

      yield item

    # Go to next page.
    next_link = response.xpath('//div[@class="border-pager"]'
                               '/div[@class="zm-invite-pager"]/span/a')
    if next_link:
      next_link = next_link[-1]
      next_link_text = next_link.xpath('./text()').extract_first().encode('utf-8')

      if next_link_text == "下一页":
        next_page_link = next_link.xpath('./@href').extract_first()
        yield scrapy.Request(
            url = urljoin(self.START_URL, next_page_link),
            headers = self.HEADERS,
            callback = self.parse
        )

