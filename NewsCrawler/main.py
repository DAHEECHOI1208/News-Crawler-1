from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from NewsCrawler.spiders.bbc_spider import BBCSpider
from NewsCrawler.spiders.cnn_spider import CNNSpider
from scrapy.utils.log import configure_logging

configure_logging()
settings = get_project_settings()

runner = CrawlerRunner(settings)

runner.crawl(BBCSpider)
runner.crawl(CNNSpider)

d = runner.join()

d.addBoth(lambda _: reactor.stop())

reactor.run()
