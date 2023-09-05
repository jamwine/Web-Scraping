import scrapy

import python_utils.scraping_utils as su
import python_utils.generic_utils as gu

class UsCompaniesWikiList(scrapy.Spider):
    name = "us_companies_url_collection"
    root_url = "https://en.wikipedia.org"

    xpath_companies = '//*[@id="mw-content-text"]'
    xpath_companies_tabular = xpath_companies + f'/div[1]/table'
    xpath_companies_categorical = xpath_companies + '/div'
    
    def _stats_print(self, data):
        print('-' * 75)
        print("Length of scraped_data: ", len(data))
        print('-' * 75)

    
    path = 'Wiki_companies/data'
    
    def start_requests(self):
        us_state_urls = gu.load_json_file(f'{self.path}/us_state_urls.json')
        us_state_urls = set(us_state_urls['us_state_urls'])
        self._stats_print(us_state_urls)
        
        for url in us_state_urls:
            print(url)
            print('-' * 75)
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response, **kwargs):
        us_companies_urls = gu.load_json_file(f'{self.path}/us_companies_urls.json')
        us_companies_urls = set(us_companies_urls['us_companies_urls'])
        
        # Extracting Tabular Urls
        print('Extracting Tabular Urls')
        max_tables = 5
        index = 0
        
        # Iterating multiple tables on webpage  
        for table in range(1, max_tables):
            print(f"Extraction from Table #{table}")
            table_headers = su.scrape_xpath(response, xpath = self.xpath_companies_tabular + f'[{table}]/tbody/tr/th/text()')

            # Identifying `Name` column in table headers
            if table_headers:
                for i, header in enumerate(table_headers, start=1):
                    header = (header.strip()).replace('\n', '')
                    if header == "Name":
                        index = i
                        break

            us_companies_tabular_urls = su.extract_urls_from_xpath(response, xpath = self.xpath_companies_tabular + f'/tbody/tr/td[{index}]/a/@href', root_url = self.root_url)
            if us_companies_tabular_urls:
                us_companies_urls = us_companies_urls.union(us_companies_tabular_urls)
            
            us_companies_tabular_italic_urls = su.extract_urls_from_xpath(response, xpath = self.xpath_companies_tabular + f'/tbody/tr/td[{index}]/i/a/@href', root_url = self.root_url)
            if us_companies_tabular_italic_urls:
                us_companies_urls = us_companies_urls.union(us_companies_tabular_italic_urls)
        
        # Extracting Categorical Urls
        print('\nExtracting Categorical Urls')
        categorical_urls = su.extract_urls_from_xpath(response, xpath = self.xpath_companies_categorical + '/ul/li/a/@href', root_url = self.root_url)
        if categorical_urls:
            us_companies_urls = us_companies_urls.union(categorical_urls)
        
        categorical_urls_in_div = su.extract_urls_from_xpath(response, xpath = self.xpath_companies_categorical + '/div/ul/li/a/@href', root_url = self.root_url)
        if categorical_urls_in_div:
            us_companies_urls = us_companies_urls.union(categorical_urls_in_div)        
        
        self._stats_print(us_companies_urls)
        gu.save_output_in_json(output_file_path = f'{self.path}/us_companies_urls.json', data = list(us_companies_urls), data_description = 'us_companies_urls')