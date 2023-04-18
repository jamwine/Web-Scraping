import scrapy
import pandas as pd
from ..items import UnlistedzonesharesItem


class UnlistedShares(scrapy.Spider):
    # Spider Initialization
    name = 'unlisted_bot1'
    start_urls = {
        'https://unlistedzone.com/shares/'
    }

    # DataFrame
    df = pd.DataFrame(columns=['company_names', 'lot_size', 'last_traded_price', 'cost_of_1_lot'])

    def parse(self, response, **kwargs):
        # Item object Creation
        items = UnlistedzonesharesItem()

        # Scraping Code using Xpath Selector
        items['company_names'] = response.xpath("//tbody[@class='table-hover']/tr/td[1]/a/text()").extract()
        items['lot_size'] = response.xpath("//tbody[@class='table-hover']/tr/td[2]/text()").extract()
        items['last_traded_price'] = response.xpath("//tbody[@class='table-hover']/tr/td[3]/text()").extract()
        items['cost_of_1_lot'] = response.xpath("//tbody[@class='table-hover']/tr/td[4]/text()").extract()
        yield items

        # Integrity validation & Transfer to DataFrame
        validate_data = [len(items['company_names']), len(items['lot_size']),
                         len(items['last_traded_price']), len(items['cost_of_1_lot'])]

        if len(set(validate_data)) == 1:
            for data in range(0, len(items['lot_size'])):
                self.df.loc[len(self.df)] = {'company_names': items['company_names'][data],
                                             'lot_size': items['lot_size'][data],
                                             'last_traded_price': items['last_traded_price'][data],
                                             'cost_of_1_lot': items['cost_of_1_lot'][data]}

        print(self.df)

        # Data Storage
        self.df.to_excel('shares_data_xpath.xlsx')
        self.df.to_json('shares_data_xpath.json')
        self.df.to_xml('shares_data_xpath.xml')

