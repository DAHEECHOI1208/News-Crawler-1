# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    visit_id = scrapy.Field()
    visit_status = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    excerpt = scrapy.Field()
    url = scrapy.Field()
    section = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    related = scrapy.Field()
    date = scrapy.Field()

    def __repr__(self):
        return repr({'url': self['url']})
