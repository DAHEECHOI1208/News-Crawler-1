from scrapy.spiders import CrawlSpider, Rule
from NewsCrawler.items import NewsCrawlerItem
from scrapy.linkextractors.sgml import SgmlLinkExtractor


class BBCSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com', 'www.bbc.co.uk']
    start_urls = [
        'http://www.bbc.com/news'
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=(r'\/news\/(?:[A-Za-z0-9]+-?)+\-(?:[0-9]+)',)), callback='parse_article', follow=True)
    ]

    def parse_article(self, response):
        story = response.css('.story-body')
        item = NewsCrawlerItem()
        if story:
            if story.css('.story-body__h1'):
                item['title'] = story.css('.story-body__h1::text').extract_first()
                item['type'] = 'Full'
                item['section'] = story.css('.mini-info-list__section::text').extract_first()
                item['content'] = story.css('p::text').extract()
                item['images'] = story.css('img').extract()
                item['related'] = story.css('.story-body__link').extract()
                item['date'] = story.css('.date::attr(data-seconds)').extract_first()

            item['url'] = response.url
        yield item
