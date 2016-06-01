import logging
from dateutil import parser as date_parser

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from NewsCrawler.items import NewsCrawlerItem


class CNNSpider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com', 'cnn.com']
    start_urls = [
        'http://edition.cnn.com'
    ]

    rules = [
        Rule(LxmlLinkExtractor(
            allow=r'\/[0-9]{4}\/[0-9]{2}\/[0-9]{2}\/[a-z]+\/(?:[a-z]+|-)+\/index.html'),
            callback='parse_article',
            follow=True)
    ]

    def parse_article(self, response):
        logging.log(logging.INFO, "Crawling: %s" % response.url)
        story = response.css('article.pg-rail-tall')
        item = NewsCrawlerItem()

        item['source'] = self.name
        item['title'] = story.css('h1.pg-headline::text').extract_first()
        item['excerpt'] = story.css('meta:nth-child(7)::attr(content)').extract_first()
        item['section'] = story.css('meta:nth-child(1)::attr(content)').extract_first()
        item['content'] = story.css('.l-container .zn-body__paragraph').xpath('text()').extract()
        item['images'] = [{"src": img.xpath('@data-src-medium').extract_first(), 'alt': self.clean_alt(img.xpath('@alt').extract_first())} for img in story.css('img').xpath('(.)[boolean(@data-src-medium)]')]
        item['related'] = [{"text": link.xpath('text()').extract_first(), "url": link.xpath('@href').extract_first()} for link in story.css('a').xpath("(.)[starts-with(@href, 'http://edition.cnn.com/')]")]
        item['date'] = date_parser.parse(story.css('meta:nth-child(4)::attr(content)').extract_first())
        item['url'] = response.url

        yield item

    @staticmethod
    def clean_alt(text):
        start = 0
        end = 0
        clean = u''
        while end >= 0:
            end = text.find('&lt;', start + 1, len(text))
            # print start, end if end >= 0 else len(text)
            clean += text[start:end if end >= 0 else len(text)]
            start = text.find('&gt;', start + 1, len(text)) + 4
        return clean.replace("&#39;", "'")
