import pandas as pd
import scrapy
from ..items import UnlistedItem
import python_utils.scraping_utils as su
import python_utils.generic_utils as gu
import pendulum
import time

class UnlistedCrawler(scrapy.Spider):
    name = 'scrape_unlisted_zone_shares'
    start_urls = {'https://unlistedzone.com/shares/'}

    xpath = "//tbody[@class='table-hover']/tr"
    company_xpath = "//*[@id='table-fill-1']/tbody/tr/td[1]/a/text()"
    lot_size_xpath = f"{xpath}/td[2]/text()"
    last_price_xpath = f"{xpath}/td[3]/text()"
    cost_per_lot_xpath = f"{xpath}/td[4]/text()"

    data = {}
    source_name = "uzs"
    today = pendulum.today().date()
    etl_date = today.to_date_string()
    output_path = "data"
    
    def parse(self, response, **kwargs):
        unlisted_item = UnlistedItem()
        unlisted_item['company'] = su.scrape_xpath(response, self.company_xpath)
        unlisted_item['lot_size'] = su.scrape_xpath(response, self.lot_size_xpath)
        unlisted_item['last_price'] = su.scrape_xpath(response, self.last_price_xpath)

        values = (unlisted_item['company'], unlisted_item['lot_size'], unlisted_item['last_price'])
            
        for i in range(len(values[0])):
            company_name = values[0][i]
            lot_size = values[1][i]
            price = values[2][i]  
        
            self.data[company_name] = {"Price": price,
                            "Lot Size": lot_size,
                            "Source": self.source_name,
                            "ETL Date": self.etl_date
                            }

        filename = f'{self.source_name}_{self.today.strftime("%Y%m%d")}'
        gu.save_output_in_json(output_file_path = f'{self.output_path}/{filename}.json', data = self.data, data_description=f'{self.source_name}_UnlistedShares')
        
        df = pd.DataFrame(self.data).T
        columns = list(df.columns)
        df = df.reset_index()
        df.columns = ["Company Name"] + columns
        df.to_csv(f'{self.output_path}/{filename}.csv', index=False)
        
        print(f"Data scraped!")