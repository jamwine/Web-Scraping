# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Cryptostock2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Stock = scrapy.Field()
    Price = scrapy.Field()
    Change = scrapy.Field()
    Percent = scrapy.Field()
    Market = scrapy.Field()
    Supply = scrapy.Field()
    Volume = scrapy.Field()
    pass
