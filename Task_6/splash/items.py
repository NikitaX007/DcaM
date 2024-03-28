# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# импортируем 3 из 6(7) обработчиков
from itemloaders.processors import TakeFirst, MapCompose, Compose
from datetime import datetime

def proccess_photos(photos):
    photos = photos.split(",")[-1].split()[0]
    return photos


def proccess_name(name):
    name = name[0].strip()
    return name

def proccess_date(date):
    date = datetime.strptime(date[0].strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
    return date


class SplashItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(proccess_photos))
    name = scrapy.Field(input_processor=Compose(proccess_name), output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(input_processor=Compose(proccess_date), output_processor=TakeFirst())
    _id = scrapy.Field()
