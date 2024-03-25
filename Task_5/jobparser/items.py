# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    vacancy_title = scrapy.Field()
    vacancy_salary = scrapy.Field()
    vacancy_experience = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    company_rate = scrapy.Field()
    company_address = scrapy.Field()
    company_location = scrapy.Field()
    description = scrapy.Field()
    vacancy_date = scrapy.Field()
    vacancy_link = scrapy.Field()
    vacancy_skills = scrapy.Field()
