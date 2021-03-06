from scrapy import Field, Item
import scrapy

class SalefinderItem(Item):
    title = Field()
    price = Field()
    per = Field()  # Per kg, each
    url = Field()
    image_url = Field()
    date = Field()
    vendor = Field()
