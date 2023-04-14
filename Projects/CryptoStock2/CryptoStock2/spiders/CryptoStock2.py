import scrapy
import pandas as pd
import time as t
from ..items import Cryptostock2Item


class SpiderCrypto(scrapy.Spider):
    # Spider Initialization
    name = 'CryptoBro2'
    handle_httpstatus_list = [404]
    df = pd.DataFrame(columns=['Stock', 'Price', 'Change', 'Percent', 'Market', 'Supply', 'Volume'])

    def start_requests(self):
        start_urls = ['https://finance.yahoo.com/crypto']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.page_index)

    def page_index(self, response):
        # User Call
        offset_mult = 4
        offset_list = [i * 25 for i in range(offset_mult)]

        # Get corresponding links
        for offset in offset_list:
            yield scrapy.Request(url=f'https://finance.yahoo.com/crypto?count=25&offset={offset}',
                                 callback=self.parse)
            t.sleep(2.5)

    def parse(self, response, **kwargs):
        # Item Instance
        crypto_item = Cryptostock2Item()

        for i in response.css('table tbody tr'):
            # Scrape all attributes
            crypto_item['Stock'] = i.css('td:nth-child(2)').css('::text').extract()[0]
            crypto_item['Price'] = i.css('td:nth-child(3) > fin-streamer:nth-child(1)').css('::text').extract()[0]
            crypto_item['Change'] = i.css('td:nth-child(4) > fin-streamer:nth-child(1) > span:nth-child(1)'). \
                css('::text').extract()[0]
            crypto_item['Percent'] = i.css('td:nth-child(5) > fin-streamer:nth-child(1) > span:nth-child(1)'). \
                css('::text').extract()[0]
            crypto_item['Market'] = i.css('td:nth-child(6) > fin-streamer:nth-child(1)').css('::text').extract()[0]
            crypto_item['Supply'] = i.css('td:nth-child(10)').css('::text').extract()[0]
            crypto_item['Volume'] = i.css('td:nth-child(8)').css('::text').extract()[0]

            yield crypto_item

            self.df.loc[len(self.df)] = crypto_item

        # Store as csv, json & xml
        self.df.to_csv("crypto_report2.csv", sep=",")
        self.df.to_json("crypto_report2.json")
        self.df.to_xml("crypto_report2.xml")

