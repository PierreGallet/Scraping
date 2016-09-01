# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbItem(scrapy.Item):
    question = scrapy.Field()
    answer = scrapy.Field()
    category = scrapy.Field()

class SfrItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()
