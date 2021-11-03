import scrapy
import json
import time
from ..items import Job51Item


class WuyouSpider(scrapy.Spider):
    name = 'wuyou'
    allowed_domains = ['51job.com']

    def start_requests(self):
        # words=['python','c++','c语言','java','nlp','人工智能','数据挖掘','web前端']
        # for word in words:
        cookie = {
            'Cookie': '_uab_collina=162788587438558439661923; guid=d9f4a9e359a8943ab4b6f4384947a4b8; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lowbrowser%3Dnot%26%7C%26; mq=java; partner=www_google_com_hk; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%D3%CE%CF%B7%BF%AA%B7%A2%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%D3%CE%CF%B7%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAgolang%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%B2%E2%CA%D4%BF%AA%B7%A2%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21; acw_sc__v2=610791306a742ad15818ae295dae91eadd93e067; acw_tc=76b20f6116278869199651820e5defed6a408e7d342aa5df45c0ff8e62b070; ssxmod_itna=Yq+xgDcD0DuQQ8Dl4iqrbD9QDyD02q2wwgqr+kBmDGN+TDZDiqAPGhDCb+IRTr8G4a3K28xqQY7mhpvQWCEmOfxjW7PweDHxY=DUgDueDxhq0rD74irDDxD3DbRdDSDWKD9D04kg9XMKDEDYP9DA3Di4D+7uQDmqG0DDtOB4G2D7t9RGxP7drU8jU3vwheoGD9D0UdxBde76uYkZaP9d2bNpI5D0pG9aw1E0DtAiiFQqGyiKGuULt/lfR1sLNleeYAKG4o/ODNmGxF3GqhQDe+DRq5A0xrIGx=QGTKQsPWRbxDG+DPU7k4eD; ssxmod_itna2=Yq+xgDcD0DuQQ8Dl4iqrbD9QDyD02q2wwgqr+kDxA6cQK4D/i7RDFrpRIB0AkYKGFnh0IxhqjEwqbp9lnQonGoTzW2tkQqbYMnU1ECmLHI7M4Plu7aHuDyS+SG80OS0LoAkzjq9UxcDSCur4SeT1Aprj22s829bdtib=+YpL=DF=I9IgZFweAis1c7K2n7riovk9lFG0ZfLZgaQXokHbadjjOyQt1WrmSLjSGIX11n=4Ll+=fOsohcrSOTis9HwFdOHxae+CuvhqhEtxxYkXPnIjhaicpFrChiwPixP4hM8mhcH0=I8kr=igQMGDDEdv2WYC53QdTddQOhTh43YzOAtf7xYDsSBOCEwM7wCgK7gzCEtlqoruK+WP9YpWxmThx7r84hIXlrFd1Kw3zA8R+3CdAWw3SuGaT5wEtmOdy7CTozZQ1XOQpko=xf4ozVQfaLLc+4bg=HnDQBIlW7FTf0e4adWd8Y6LtF610cWqo1LkYCwDxc4X=aLDDwrGi0eC4h07D0CB8cPPLeKXqPDeCb2yA4Q+Gga+5LmKGqeWvirxDjKDeTx4D==='
        }
        for page in range(1, 1148):
            url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python开发,2,{}.html?' \
                  'lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99'.format(page)
            time.sleep(0.5)
            yield scrapy.Request(url=url, cookies=cookie, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            html = response.xpath('/html/body/script[2]/text()').extract_first()[29:]
            data = json.loads(html)
            result_list = data.get('engine_jds', [])
            for res in result_list:
                item = Job51Item()
                # item = {}
                # item['coid'] = res.get('coid', -1)
                item['job_name'] = res.get('job_name', -1)
                item['company_name'] = res.get('company_name', -1)
                salary = res.get('providesalary_text')
                if not salary is None:
                    item['salary'] = salary_range(sal_transform(salary))
                    item['avg_salary'] = sal_transform(salary)
                else:
                    item['salary'] = '面议'
                attribute_text = res.get('attribute_text', -1)
                item['address'] = address_transform(attribute_text[0])
                if len(attribute_text) > 3:
                    item['work_year'] = attribute_text[1]
                    item['education'] = attribute_text[2]
                else:
                    item['work_year'] = '无需经验'
                    item['education'] = '无要求'
                item['issuedate'] = res.get('issuedate', -1)
                job_welf = res.get('jobwelf', )
                if job_welf:
                    item['jobwelf'] = job_welf
                else:
                    item['jobwelf'] = '无福利'
                item['companysize'] = res.get('companysize_text', -1)
                item['job_href'] = res.get('job_href', -1)
                yield item
                # else:
                print("************当前是第%s页****************" % data['curr_page'])


def address_transform(s):
    if '-' in s:
        address = s.split('-')[0]
        return address
    else:
        return s


def sal_transform(s):
    if s.endswith('月'):
        data = s.split('/')[0]
        if data.endswith('万'):
            sal = data.split('-')
            min = int(float(sal[0]) * 10000)
            max = int(float(sal[1].replace('万', '')) * 10000)
            avg = (min + max) / 2
            return int(avg)
        if data.endswith('千'):
            sal = data.split('-')
            min = int(float(sal[0]) * 1000)
            max = float(sal[1].replace('千', '')) * 1000
            avg = (min + max) / 2
            return int(avg)
    if s.endswith('年'):
        data = s.split('/')[0]
        if data.endswith("万"):
            sal = data.split("-")
            min = float(sal[0]) * 10000 / 12
            max = float(sal[1].replace('万', '')) * 10000 / 12
            avg = int((min + max) / 2)
            return int(avg)
    if s.endswith('天'):
        data = s.split('/')[0]
        avg = float(data.replace('元', '')) * 30
        return int(avg)
    if s.endswith('时'):
        data = s.split("/")[0]
        avg = float(data.replace('元', '')) * 8 * 30
        return int(avg)
    else:
        s = 3000
        return s


def salary_range(s):
    if s > 0 and s <= 5000:
        salary = '0-5k'
        return salary
    if 5000 < s and s <= 10000:
        salary = '5-10k'
        return salary
    if 10000 < s and s <= 15000:
        salary = '10k-15k'
        return salary
    if 15000 < s and s <= 20000:
        salary = '15k-20k'
        return salary
    if 20000 < s and s <= 30000:
        salary = '20k-30k'
        return salary
    if 3000 < s and s <= 40000:
        salary = '30k-40k'
        return salary
    else:
        salary = '40k以上'
        return salary
