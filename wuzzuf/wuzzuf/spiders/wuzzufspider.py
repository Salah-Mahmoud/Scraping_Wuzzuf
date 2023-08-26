from urllib.parse import urlencode

import scrapy

API_KEY = '298e61c7-e6a7-4b45-9670-83c252529c08'


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class WuzzufSpider(scrapy.Spider):
    name = "wuzzufspider"
    allowed_domains = ["wuzzuf.net"]
    page_number = 1
    start_url = 'https://wuzzuf.net/search/jobs/?a=hpb&q=data%20science&start=0'

    def start_requests(self):
        start_url = 'https://wuzzuf.net/search/jobs/?a=hpb&q=data%20science&start=0'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)

    def parse(self, response):
        jobs = response.css('div.css-pkv5jc')
        for job in jobs:
            yield {
                'Title': job.css('h2 a::text').get(),
                'Location': job.css('.css-5wys0k ::text').getall(),
                'Job_Type': job.css('.css-1ve4b75.eoyjyou0::text').get(),
                'Exp_level': job.css('.css-o171kl::text')[1].get(),
                'Exp_year': job.css('.css-y4udm8 > div:nth-child(2) span::text').get(),
            }

        next_page = f'https://wuzzuf.net/search/jobs/?a=navbg&filters%5Bcountry%5D%5B0%5D=Egypt&q=data%20science&start={self.page_number}'
        if self.page_number <= 37:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
