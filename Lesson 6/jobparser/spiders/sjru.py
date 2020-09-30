
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search = 'python'
    start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        vacancy_links = response.xpath('//div[@class="_3zucV _1fMKr undefined _1NAsu"]/*/*/*/*/*/*/a/@href').extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(selfself, response: HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        salary_job = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        location_job = response.xpath('//div[@class="f-test-address _3AQrx"]//text()').extract()
        position_link = response.url
        company_job = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc _2VHxz"]/text() |'
                                     ' //h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)
