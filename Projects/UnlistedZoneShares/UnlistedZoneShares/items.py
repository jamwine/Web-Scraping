# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnlistedzonesharesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_names = scrapy.Field()
    lot_size = scrapy.Field()
    last_traded_price = scrapy.Field()
    cost_of_1_lot = scrapy.Field()
    pass
