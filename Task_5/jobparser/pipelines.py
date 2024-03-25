# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from tokens import ATLAS_USER, ATLAS_PASS, ATLAS_HOST
class JobparserPipeline:
    def __init__(self):
        uri = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@cluster0.{ATLAS_HOST}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri)
        self.mongobase = client["vacancies"]

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item
