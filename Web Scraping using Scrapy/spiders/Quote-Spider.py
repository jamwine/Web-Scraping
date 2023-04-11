import scrapy


# Inherit the Spider module from scrapy
class QuoteSpider(scrapy.Spider):
    # Initialize bot name and the starting urls
    name = 'SpiderQuote'
    start_urls = {
        'https://quotes.toscrape.com/'
    }

    def parse(self, response, **kwargs):
        # define an empty list
        tags = []

        # Extract the specific Information
        quotes = response.css('.text::text').extract()
        authors = response.css('.author::text').extract()
        selector = response.css('div.tags')

        # Locate all the tags for a single quote upon each iteration
        for i in selector:
            collection_list = i.css('a::text').extract()
            # Join each element of the list for a single quote & store inside the list to maintain homogenous structure
            tags.append(' '.join(collection_list))

        yield {'Quotes': quotes, 'Authors': authors, 'Tags': tags}
