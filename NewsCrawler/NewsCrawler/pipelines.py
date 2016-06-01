from scrapy.exceptions import DropItem
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import pymongo, datetime


class NewsCrawlerPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.stemmer = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['documents'].ensure_index('url', unique=True)
        self.db['dictionary'].ensure_index('term', unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['title']:
            if self.db['documents'].find({'url': item['url']}).count() == 0:
                tokens = []
                for paragraph in item['content']:
                    tokens += self.tokenize_and_stem(paragraph)
                tokens += self.tokenize_and_stem(item['title'])
                tf = Counter(tokens)
                document_id = self.db['documents'].insert({
                    'source': item['source'],
                    'title': item['title'],
                    'excerpt': item['excerpt'],
                    'url': item['url'],
                    'section': item['section'],
                    'images': item['images'],
                    'related': item['related'],
                    'date': item['date'],
                    'crawled_at': datetime.datetime.utcnow()
                })
                bulk = self.db['dictionary'].initialize_unordered_bulk_op()
                for key in tf:
                    bulk.find({'term': key}).upsert().update_one({
                        '$set': {
                            'term': key
                        },
                        '$currentDate': {
                            'lastModified': True
                        },
                        '$inc': {
                            'freq': tf[key]
                        }
                    })
                bulk.execute()
                terms = [term for term in tf]
                results = self.db['dictionary'].find({'term': {'$in': terms}}, {'_id': 1, 'term': 1})
                bulk = self.db['postings'].initialize_unordered_bulk_op()
                for result in results:
                    bulk.insert({'document_id': document_id, 'term_id': result['_id'], 'freq': tf[result['term']]})
                bulk.execute()
                return item
            else:
                raise DropItem("This page has been crawled and processed %s" % item['title'])
        else:
            raise DropItem("Its not an story")

    def tokenize_and_stem(self, s):
        return [self.stemmer.stem(word) for word in self.tokenizer.tokenize(s.lower()) if
                word not in stopwords.words('english')]
