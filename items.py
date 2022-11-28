# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazonSellersItem(scrapy.Item):
    seller_name = scrapy.Field()
    biz_name = scrapy.Field()
    biz_type = scrapy.Field()
    rating_star = scrapy.Field()
    rating = scrapy.Field()
    biz_address = scrapy.Field()
    customer_service_address = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    seller_link = scrapy.Field()
    marketplace = scrapy.Field()

class SellersItem(scrapy.Item):
    of_product_link = scrapy.Field()
    of_seller_link = scrapy.Field()

class ASINsItem(scrapy.Item):
    asin = scrapy.Field()

