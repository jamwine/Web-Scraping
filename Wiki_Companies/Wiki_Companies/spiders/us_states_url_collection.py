import scrapy

import python_utils.scraping_utils as su
import python_utils.generic_utils as gu

class UsStatesWikiList(scrapy.Spider):
    name = "us_states_url_collection"
    root_url = "https://en.wikipedia.org"
    start_urls = ["https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States_by_state"]
    
    xpath_companies = '//*[@id="mw-content-text"]/div[1]/div/'
    path = 'Wiki_companies/data'

    def _stats_print(self, data):
        print('-' * 75)
        print("Length of scraped_data: ", len(data))
        print('-' * 75)


    def parse(self, response, **kwargs):
        
        us_state_urls = su.extract_urls_from_xpath(response, xpath = self.xpath_companies + 'a/@href', root_url = self.root_url)
        if us_state_urls:
            self._stats_print(us_state_urls)
            gu.save_output_in_json(output_file_path = f'{self.path}/us_state_urls.json', data = list(us_state_urls), data_description = 'us_state_urls')
        
        us_companies_urls = su.extract_urls_from_xpath(response, xpath = self.xpath_companies + 'ul/li/a/@href', root_url = self.root_url)
        if us_companies_urls:
            self._stats_print(us_companies_urls)
            gu.save_output_in_json(output_file_path = f'{self.path}/us_companies_urls.json', data = list(us_companies_urls), data_description = 'us_companies_urls')