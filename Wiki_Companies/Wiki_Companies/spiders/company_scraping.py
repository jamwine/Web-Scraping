import scrapy
import json
import python_utils.generic_utils as gu

class CompanyScrapingSpider(scrapy.Spider):
    name = "company_scraping"
    root_url = "en.wikipedia.org"
    path = 'Wiki_companies/data'
    
    
    def start_requests(self):
        us_companies_urls = gu.load_json_file(f'{self.path}/us_companies_urls.json')
        us_companies_urls = set(us_companies_urls['us_companies_urls'])
        # self._stats_print(us_companies_urls)
        
        # Create an empty JSON object
        data = {}

        # Write the empty JSON object to the file
        with open(f'{self.path}/company_scraping.json', 'w') as json_file:
            json.dump(data, json_file)
        print(f"Empty JSON file created at {self.path}/company_scraping.json")

        for url in us_companies_urls:
            print(url)
            print('-' * 75)
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response):
        company_data = gu.load_json_file(f'{self.path}/company_scraping.json')
        try:
            company_data = company_data['data']
        except:
            company_data = {}
        # Find the tbody element
        tbody = response.css('.infobox tbody')
        
        output_dict = {}
        temp_dict = {}
        # Iterate over each tr tag within tbody
        for row in tbody.css('tr'):
            label = row.xpath('.//th//text()').get()
            data = row.xpath('.//td//text()').getall()

            # Clean up label and data
            label = label.strip() if label else ''
            data = [item.strip() for item in data]

            if label:
                temp_dict[label] = data
        print("-----------------")

        output_dict[(response.request.url).split('/')[-1]] = temp_dict
        company_data.update(output_dict)
        
        gu.save_output_in_json(output_file_path = f'{self.path}/company_scraping.json', data = company_data)