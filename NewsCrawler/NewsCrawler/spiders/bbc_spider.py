import datetime
import logging

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from NewsCrawler.items import NewsCrawlerItem


class BBCSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com', 'www.bbc.co.uk']
    start_urls = [
        'http://www.bbc.com/news'
    ]

    rules = [
        Rule(LxmlLinkExtractor(
            allow=(r'\/news\/(?:[A-Za-z0-9]+-?)+\-(?:[0-9]+)',),
            restrict_xpaths='//*[@id="page"]',
            deny=r'\/news\/help\-(?:[0-9]+)'),
            callback='parse_article',
            follow=True)
    ]

    def parse_article(self, response):
        logging.log(logging.INFO, "Crawling: %s" % response.url)
        story = response.css('.story-body')
        item = NewsCrawlerItem()

        item['source'] = self.name
        item['title'] = story.css('.story-body__h1::text').extract_first()
        item['excerpt'] = story.css('.story-body__introduction::text').extract_first()
        item['section'] = story.css('.mini-info-list__section::text').extract_first()
        item['content'] = story.css('p::text').extract()
        images = [img for img in story.css('figure').xpath('span/img|span/div[1]').xpath('@alt|@data-alt').extract()]
        item['images'] = [{"src": img, 'alt': images[i]} for i, img in enumerate(story.css('figure').xpath('span/img|span/div[1]').xpath('@src|@data-src').extract())]
        item['related'] = [{'text': link.xpath('text()').extract_first(), 'url': link.xpath('@href').extract_first()} for link in story.css('.story-body__link')]
        item['date'] = datetime.datetime.fromtimestamp(int(story.css('.date::attr(data-seconds)').extract_first()))
        item['url'] = response.url

        yield item
