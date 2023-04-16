import scrapy


class SpiderPython(scrapy.Spider):
    name = 'Spider-Python'
    start_urls = {
        'https://www.python.org/events/python-events/'
    }

    def parse(self, response, **kwargs):
        # Transitioning through all classes in sequential order by using .css selector
        upcoming_events = response.css('.shrubbery .event-title a::text').extract()
        location = response.css('.shrubbery .event-location::text').extract()
        date = response.css('.shrubbery time::text').extract()

        yield {'Upcoming Events': upcoming_events, 'Location': location, 'Date': date}

