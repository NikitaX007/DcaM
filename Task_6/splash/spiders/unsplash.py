import scrapy
from scrapy.http import HtmlResponse
from splash.items import SplashItem
from scrapy.loader import ItemLoader


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    protocol = 'https://'
    folder = '/photos'
    # вместо start_urls = ["https://unsplash.com"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"{self.protocol}{self.allowed_domains[0]}/s{self.folder}/{kwargs.get('query')}"]

    def parse(self, response):
        # вместо pass добавляем 
        links = response.xpath('//a[@itemprop="contentUrl"]/@href').getall()
        for link in links:
            link = self.protocol + self.allowed_domains[0] + link
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response: HtmlResponse):
        loader = ItemLoader(item=SplashItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('photos', '//button//img/@srcset')
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('description', '//p[@style]/text()')
        loader.add_xpath('date', '//time/@datetime')
        yield loader.load_item()