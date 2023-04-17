import scrapy
import pandas as pd
from ..items import Scrapy1Item
import time as t


class RedditScraping(scrapy.Spider):
    # Spider
    name = 'RedditBot1'

    # Pagination
    start_urls = {
        'https://www.reddit.com/r/webscraping/',
        'https://www.reddit.com/r/webscraping/?after=t3_12kddea',
        'https://www.reddit.com/r/webscraping/?after=t3_12f3mpp'
    }

    # Data Frame
    df = pd.DataFrame(columns=['titles', 'descriptions', 'votes'])

    def parse(self, response, **kwargs):
        # Items Object
        items = Scrapy1Item()

        # Scraping Code
        titles = response.css('div > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > h3:nth-child(1)')\
            .css('::text').extract()
        descriptions = response.css('div > div:nth-child(3) > div:nth-child(3) > a:nth-child(1) > div:nth-child(1) > '
                                    'div:nth-child(1)')
        check_ads = response.css('div > div:nth-child(3) > div:nth-child(1)')
        votes = response.css('div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)::text').extract()

        description_list = []
        for description in descriptions:
            temp = description.css('p').css('::text').extract()
            description_list.append("".join(temp))

        #  Experimental Code: Detect Ads
        if check_ads:
            print('Ad detected')
            ads_link = check_ads.css('div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > '
                                     'a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > '
                                     'img:nth-child(1)::attr(src)').extract_first()
            # titles.pop(1) Block Ads
            # votes.pop(1) Block Ads

        items['titles'] = titles
        items['descriptions'] = description_list
        items['votes'] = votes

        if len(titles) == len(description_list) and len(titles) == len(description_list):
            for i in range(0, len(items['titles'])):
                self.df.loc[len(self.df)] = \
                    {'titles': items['titles'][i], 'descriptions': items['descriptions'][i], 'votes': items['votes'][i]}

            # Save as storage
            self.df.to_excel("reddit.xlsx")
            self.df.to_json("reddit.json")
            self.df.to_xml("reddit.xml")
        t.sleep(2)

