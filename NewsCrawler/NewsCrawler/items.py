# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    excerpt = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    section = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    related = scrapy.Field()
    date = scrapy.Field()

