# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):
    table_name = 'job51'
    # coid = scrapy.Field()
    job_name = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    avg_salary = scrapy.Field()
    address = scrapy.Field()
    work_year = scrapy.Field()
    education = scrapy.Field()
    issuedate = scrapy.Field()
    jobwelf = scrapy.Field()
    companysize = scrapy.Field()
    job_href = scrapy.Field()


class LiepinItem(scrapy.Item):
    table_name = 'liepin'
    keyword = scrapy.Field()
    job_name = scrapy.Field()
    salary = scrapy.Field()
    avg_salary = scrapy.Field()
    address = scrapy.Field()
    eduction = scrapy.Field()
    work_year = scrapy.Field()
    company_size = scrapy.Field()
    company_name = scrapy.Field()


class YingjieItem(scrapy.Item):
    name = scrapy.Field()
    position_desc = scrapy.Field()
