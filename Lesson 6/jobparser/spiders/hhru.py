import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    search = 'puyhon'

    start_urls = [f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={search}&showClusters=true']

    def parse(self, response: HtmlResponse):

        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()

        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)


        yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        salary_job = response.css('p.vacancy-salary span::text').extract()
        location_job = response.xpath('//p[@data-qa="vacancy-view-location"]//text()').extract()
        position_link = response.url
        company_job = response.xpath('//span[@class="bloko-section-header-2 bloko-section-header-2_lite"]/text()').extract()
        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)
