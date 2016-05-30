from scrapy.exceptions import DropItem


class NewscrawlerPipeline(object):
    def process_item(self, item, spider):
        if item['title']:
            return item
        else:
            raise DropItem("Its not an story %s" % item)
