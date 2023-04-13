# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YhfinanceItem(scrapy.Item):
    # define the fields for your item here like:
    stock_name = scrapy.Field()
    price_day = scrapy.Field()
    price_chg = scrapy.Field()
    perc_chg = scrapy.Field()
    market_cap = scrapy.Field()
    circ_supply = scrapy.Field()
    volume = scrapy.Field()
    # name = scrapy.Field()
    pass
