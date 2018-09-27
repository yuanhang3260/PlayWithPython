# -*- coding: utf-8 -*-
import scrapy

from douban.items import MovieItem

class TopmoviesSpider(scrapy.Spider):
  name = 'topMovies'
  allowed_domains = ['movie.douban.com/top250']
  start_urls = ['https://movie.douban.com/top250']

  def parse(self, response):
    # print response.text

    movies = response.xpath('//*[@id="content"]//div[@class="article"]//ol[@class="grid_view"]/li');
    for movie in movies:
      movie_item = MovieItem()
      movie_item["name"] = movie.xpath('.//div[@class="hd"]/a/span[@class="title"]/text()').extract_first().strip()
      movie_item["description"] = movie.xpath('.//div[@class="bd"]/p/text()').extract_first().strip(u'"').strip()
      print movie_item["description"]
      yield movie_item

    # Go to next page.
    next_link = response.xpath('//*[@id="content"]//div[@class="article"]//span[@class="next"]/link/@href').extract();
    if next_link:
      yield scrapy.Request(TopmoviesSpider.start_urls[0] + next_link[0], callback=self.parse, dont_filter=True)
