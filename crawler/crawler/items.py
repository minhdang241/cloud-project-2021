# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Course(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    outcome = scrapy.Field()
    pass
