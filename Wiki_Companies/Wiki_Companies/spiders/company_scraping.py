import scrapy

import python_utils.generic_utils as gu

class CompanyScrapingSpider(scrapy.Spider):
    name = "company_scraping"
    root_url = "en.wikipedia.org"

    def start_requests(self):
        us_companies_urls = gu.load_json_file('data/us_companies_urls.json')
        us_companies_urls = set(us_companies_urls['us_companies_urls'])
        # self._stats_print(us_companies_urls)
        
        for url in us_companies_urls:
            print(url)
            print('-' * 75)
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response):
        company_data = gu.load_json_file('data/company_scraping.json')
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
        
        gu.save_output_in_json(output_file_path = 'data/company_scraping.json', data = company_data)