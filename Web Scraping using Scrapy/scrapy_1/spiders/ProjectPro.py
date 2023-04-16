import time as t
import scrapy
import pandas as pd
from ..items import Scrapy1Item


class ProjectPro(scrapy.Spider):
    # Spider initialization
    name = 'project_pro1'
    df = pd.DataFrame(columns=['projects', 'dates', 'links'])

    def start_requests(self):
        # Initiate a request for pagination
        start_urls = ['https://www.projectpro.io/blog']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.get_index)

    def get_index(self, response):
        # Crawling Setups
        page_limit = 7

        for page_number in range(1, page_limit + 1):
            t.sleep(3)
            indexed_url = f'https://www.projectpro.io/blog/page_no/{page_number}'
            yield scrapy.Request(url=indexed_url, callback=self.parse)

    def parse(self, response, **kwargs):
        # Items Object
        items = Scrapy1Item()

        # Scraping Code
        titles = response.css('div.p-3 > h1:nth-child(1) > a:nth-child(1)').css('::text').extract()
        items['dates'] = response.css('div.p-3 > time:nth-child(5)').css('::text').extract()
        items['links'] = response.css('div.p-3 > div:nth-child(6) > p:nth-child(1) > img::attr(data-src)').extract()

        title_list = []
        for title in titles:
            title_list.append(title.strip())

        items['projects'] = title_list

        # Store each element in the DataFrame
        for i in range(0, len(items['projects'])):
            self.df.loc[len(self.df)] = \
                {'projects': items['projects'][i], 'dates': items['dates'][i], 'links': items['links'][i]}

        # Save as storage
        self.df.to_excel("project_pro.xlsx")
        self.df.to_json("project_pro.json")
        self.df.to_xml("project_pro.xml")




