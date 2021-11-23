import scrapy
from scrapy.http import Request

class YincaiSpider(scrapy.Spider):
    name = 'Yincai'
    allowed_domains = ['campus.chinahr.com']
    # start_urls = ['http://campus.chinahr.com/']

    def start_requests(self):
        url = 'http://campus.chinahr.com/qz?keyword={}&city=1&currentpage=1'
        words = ['java','python','运维','测试']
        for word in words:
            yield Request(url.format(word),callback=self.parse)

    def parse(self, response):
        selectors = response.xpath('//dl[@class="job-list"]/dd')
        for selector in selectors:
            item = {}
            item['job_name'] = selector.xpath('.//div[1]/a/text()').extract_first()
            item['salary'] = selector.xpath('.//div[@class="job-info"]/strong[@class="job-salary"]/text()').extract_first()
            item['address'] = address_transform(selector.xpath('.//div[@class="job-info"]/span[1]/text()').extract_first())
            item['company_name'] = selector.xpath('.//div[@class="top-area"]/span/text()').extract_first()
            href = "http://campus.chinahr.com/"+selector.xpath('./div[1]/a/@href').extract_first()
            next_url = response.xpath('//div[@class="pagination-bar"]/a[last()]/@href').extract_first()
            if not 'javascript:;' in next_url:
                next_url = "http://campus.chinahr.com/"+response.xpath('//div[@class="pagination-bar"]/a[last()]/@href').extract_first()
                yield Request(next_url,callback=self.parse)
            else:
                ''
            yield Request(href,meta={'item':item},callback=self.parse_detail)

    def parse_detail(self,response):
        item = response.meta['item']
        item['position_desc'] = position_transform(response.xpath('//div[@class="job-responsibility"]/p/text()').extract())
        print(item)
        return item

def position_transform(s):
    return ','.join(s).strip().replace('\n','')

def address_transform(s):
    return ''.join(s).strip().replace('\r\n','')