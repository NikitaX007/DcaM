#!/usr/bin/env python
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from splash.spiders.unsplash import UnsplashSpider
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    query = input("Введите тему для поиска: ").replace(' ', '-')
    configure_logging()
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    configure_logging
    settings = get_project_settings()
    settings.set('IMAGES_STORE', query)
    settings.set('FEED_EXPORT_FIELDS', ['name', 'photos', 'description', 'date'])
    settings.set('FEEDS', {
                            query+'.csv': {
                                'format': 'csv',
                                'item_export_kwargs': {
                                    'include_headers_line': False,
                                    'delimiter': '\t',  
                                },
                            }})
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Proxy list path")
    args = parser.parse_args()
    if args.path:
        settings.set('ROTATING_PROXY_LIST_PATH', args.path)
        settings.set('DOWNLOADER_MIDDLEWARES', {
   'rotating_proxies.middlewares.RotatingProxyMiddleware': 100,
   'rotating_proxies.middlewares.BanDetectionMiddleware': 110,
                    })

    process = CrawlerProcess(settings=settings)
    process.crawl(UnsplashSpider, query=query)
    process.start()