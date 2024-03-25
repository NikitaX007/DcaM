import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from datetime import datetime # библиотека для работы с форматами дат, нужна для преобразования из строк
import locale # библиотека для работы с локализацией, необходима для правильного преобразования русских месяцев
locale.setlocale(locale.LC_TIME, 'ru_RU.utf8') # указываю русскую локализацию, для преобразования месяцев


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    protocols = ["https"]
    #text = "python"
    text = input("Введите вакансию: ")
    #area = 1 # 1 - Москва, 2 - Санкт-Петербург, 0 - все
    try: 
        area = int(input("Индекс региона (1. Москва, 2. С.Петербург ..., 0. поиск везде): "))
    except:
        print("He правильно введен индекс региона")
    path = "/search/"
    file = "vacancy"
    start_urls = [f"{protocols[0]}://{allowed_domains[0]}{path}{file}?text={text}&area={area}&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[contains(@href, "hh.ru/vacancy/")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
              
    def vacancy_parse(self, response: HtmlResponse):
        vacancy_title = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        try:
            vacancy_salary = response.xpath('.//div[@data-qa="vacancy-salary"]//text()').getall()
            vacancy_salary = [x.strip() for x in vacancy_salary]
            vacancy_salary = [x.replace('₽', 'руб.') for x in vacancy_salary]
            vacancy_salary[1] = int(vacancy_salary[1].replace('\xa0', ''))
            vacancy_salary[3] = int(vacancy_salary[3].replace('\xa0', ''))
        except:
            vacancy_salary = []
        vacancy_experience = response.xpath(".//p[@class='vacancy-description-list-item']//text()").getall()
        vacancy_experience = [x for x in vacancy_experience if x != ', ' and x != ': ']
        company_name = response.xpath('.//a[@data-qa="vacancy-company-name"]/span/text()').getall()
        company_name = list(set([x.replace('\xa0', '') for x in company_name]))
        company_link = self.protocols[0]+'://'+self.allowed_domains[0] + response.xpath('.//a[@data-qa="vacancy-company-name"]/@href').get()
        try:
            company_rate = float(response.xpath('.//div[@data-qa="employer-review-small-widget-total-rating"]/text()').get().replace(",", "."))
        except:
            company_rate = ''
        company_address = response.xpath('.//span[@data-qa="vacancy-view-raw-address"]//text()').getall()
        if len(company_address) == 0:
            company_address = response.xpath(".//p[@data-qa='vacancy-view-location']/text()").getall()
        company_address = list(set([x.replace(',', '').strip() for x in company_address if x != '' and x != ', ']))
        description = response.xpath(".//div[@data-qa='vacancy-description']//text()").getall()
        description = [x.replace('\xa0', '') for x in description if x != ', ' and x != ' ' and x != ' ']
        vacancy_date = response.xpath('.//p[@class="vacancy-creation-time-redesigned"]/span/text()').get().replace('\xa0', ' ')
        vacancy_date = datetime.strptime(vacancy_date, '%d %B %Y').strftime('%Y-%m-%d')
        vacancy_link = response.url
        vacancy_skills = response.xpath('.//div[@class="bloko-tag-list"]//text()').getall()
        _id = int(vacancy_link.split('/')[-1].split('?')[0])
        yield JobparserItem(_id=_id, vacancy_title=vacancy_title, vacancy_salary=vacancy_salary, vacancy_experience=vacancy_experience, 
                            company_name=company_name, company_link=company_link, company_rate=company_rate, 
                            company_address=company_address, description=description, 
                            vacancy_date=vacancy_date, vacancy_link=vacancy_link, vacancy_skills=vacancy_skills)
        
