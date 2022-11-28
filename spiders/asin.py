# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from ..items import ASINsItem

class ASINsSpider(scrapy.Spider):
    name = 'asin'

    # read file to get best sellers url
    with open('best_sellers_url.txt', 'r') as f:
       bs_url = f.readline()

    start_urls = [bs_url]

    def parse(self, response):  # parse 100 products ASIN numbers
        items = ASINsItem()
        # find all products link
        product_links = response.xpath(
              "//*[@id = 'zg-ordered-list']//span[@class = 'aok-inline-block zg-item']/a[1]/@href").getall()
        for url in product_links: # parse urls to get ASIN numbers
            print(url)
            items['asin'] = urlparse(url).path.split('/')[-3] # sometimes it get nasty, we should count backwards
            yield items

        yield from response.follow_all(css='li.a-last a', callback=self.parse)

