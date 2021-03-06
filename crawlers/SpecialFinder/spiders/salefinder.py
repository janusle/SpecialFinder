# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from datetime import date

from SpecialFinder.items import SalefinderItem


class SaleFinderSpider(CrawlSpider):
    name = 'salefinder'
    allowed_domains = ['salefinder.com.au']
    start_urls = ['http://salefinder.com.au/coles-catalogue/',
                  'http://salefinder.com.au/Woolworths-catalogue/']
    next_page_xpath =\
        r"//div[@class='pagenumbers']//a[@class='pagenumsblack' and contains(text(), 'Next')]"
    item_xpath =\
        r"//div[@class='item-landscape']//a[@class='item-name']"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=next_page_xpath)),
        Rule(LinkExtractor(restrict_xpaths=item_xpath),
                           callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # FIXME: fix array issue
        i = ItemLoader(item=SalefinderItem(), response=response)
        title = r'//div[@id="product-details-container"]//h1/text()'
        price = r'//div[@id="product-details-container"]//span[@class="price"]/text()'
        per = r'//div[@id="product-details-container"]//span[@class="price"]/text()'
        image_url = r'//a[@id="product-image-container"]//img/@src'

        i.add_xpath('title', title, MapCompose(unicode.lower))
        i.add_xpath('price', price, re=r'[,.0-9]+')
        i.add_xpath('per', per, re=r'pk|each|kg')
        i.add_xpath('image_url', image_url)

        i.add_value('url', response.url)
        i.add_value('date', date.today().isoformat())

        product_buy = response.xpath("//div[@class='product-container']//div[@id='product-buy']")
        product_buy_text = product_buy.extract_first().lower()

        # Detect the vendor from a product-buy div
        if 'coles' in product_buy_text:
            i.add_value('vendor', 'coles')
        elif 'woolworths' in product_buy_text:
            i.add_value('vendor', 'woolworths')
        else:
            i.add_value('vendor', 'unknown')
        return i.load_item()
