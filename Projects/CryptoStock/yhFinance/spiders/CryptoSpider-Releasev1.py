#Work in Progress, later updates will follow

import scrapy
import time as t
import pandas as pd
from ..items import YhfinanceItem


class SpiderCrypto(scrapy.Spider):
    # Spider
    name = 'CryptoBro1'
    # 404 Handler
    handle_httpstatus_list = [404]
    df = pd.DataFrame(columns=['stock_name', 'price_day', 'price_chg', 'perc_chg', 'market_cap', 'circ_supply',
                               'volume'])

    def start_requests(self):
        # Main url
        start_urls = ['https://finance.yahoo.com/crypto']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.page_extraction)

    def page_extraction(self, response):
        filter = str(response.xpath('//html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[1]/div[1]/span[2]/span').css(
            '::text').extract())
        print(filter)

        results = int(filter.split()[-2])
        offsets = results // 25 + 1
		offsets_override = 11
        list_offsets = [i * 25 for i in range(offsets)]
        for offset in list_offsets:
            t.sleep(3)
            yield scrapy.Request(url=f'https://finance.yahoo.com/crypto?count=25&offset={offset}',
                                 callback=self.stock_pg)

    def stock_pg(self, response):
        # Get all the stocks from the Main
        stocks = response.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody//tr/td[1]/a').css('::text').extract()
        for stock in stocks:
            t.sleep(3)
            # Crawl to each individual Stock Page.
            yield scrapy.Request(url=f'https://finance.yahoo.com/quote/{stock}?p={stock}', callback=self.parse)

    def parse(self, response, **kwargs):
        # Item Instance
        items = YhfinanceItem()

        # Scrape all attributes
        items['stock_name'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div'
                                             '/div[2]/div[1]/div[1]/h1/text()').extract()
        items['price_day'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div'
                                            '/div[3]/div[1]/div/fin-streamer[1]/text()').extract()
        items['price_chg'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/'
                                            'div[3]/div[1]/div/fin-streamer[2]/span/text()').extract()
        items['perc_chg'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/'
                                           'div[3]/div[1]/div/fin-streamer[3]/span/text()').extract()
        items['market_cap'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/'
                                             'div/div[2]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()
        items['circ_supply'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/'
                                              'div/div[2]/div[2]/table/tbody/tr[2]/td[2]/text()').extract()
        items['volume'] = response.xpath('/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div'
                                         '/div[2]/div[2]/table/tbody/tr[4]/td[2]/fin-streamer/text()').extract()
        yield items
		
        self.df.loc[len(self.df)] = items
        self.df.to_csv("crypto_report1.csv", sep=",")

		
