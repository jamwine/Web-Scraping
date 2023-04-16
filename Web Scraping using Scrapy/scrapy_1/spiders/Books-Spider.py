import scrapy
import time


class SpiderBook(scrapy.Spider):
    name = 'Spider-Book'
    # Simple Pagination Web links
    start_urls = {
        'https://books.toscrape.com/catalogue/page-%d.html' % i for i in range(1, 51)
    }

    def parse(self, response, **kwargs):
        book_title = []
        selector = response.css('.row .product_pod')

        for i in selector:
            # Finds & Stores the Title of the books for all 50 pages
            books = i.css('h3 a').attrib['title']
            book_title.append(books)

            # 1s Sleep is applied to ensure efficacy as well as avoiding 403/404 errors
            time.sleep(1)

        yield {'All Available Books': book_title}
