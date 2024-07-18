# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy.item import Field,Item
# import scrapy.item


# class TutorialItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class BookDetail(Item):
    title = Field()
    price = Field()
    description = Field()
    cateogry = Field()
    availability = Field()
    upc = Field()
    rating = Field()
    last_updated_dt = Field()
  