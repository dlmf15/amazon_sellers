# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from ..items import SellersItem

class SellersLinksSpider(scrapy.Spider):
    name = 'sellers_links'
    
    # read file to get best sellers url
    with open('best_sellers_url.txt', 'r') as f:
        bs_url = f.readline()

    start_urls = [bs_url]

    def parse(self, response):# parse 100 products ASIN numbers

        # find all products link
        product_links = response.xpath(
            "//*[@id = 'zg-ordered-list']//span[@class = 'aok-inline-block zg-item']/a[1]/@href").getall()
        
        for url in product_links: # parse urls to get ASIN numbers
            asin = urlparse(url).path.split('/')[3]
            
            # use ASIN number to generate offer-listing url
            offer_list_link = 'https://www.amazon.de/gp/offer-listing/' + asin \
                             + '/ref=dp_olp_all_mbc?ie=UTF8&condition=all'
            yield scrapy.Request(offer_list_link, callback=self.parse_offer)

        #product_links = response.xpath(
        #    "//*[@id = 'zg-ordered-list']//span[@class = 'aok-inline-block zg-item']/a[1]/@href")

        #yield from response.follow_all(product_links, callback=self.parse_product)

        yield from response.follow_all(css='li.a-last a', callback=self.parse)

    def parse_product(self, response):  # product page
        offer_link = response.xpath("//a[contains(@href,'offer-listing')]/@href")
        if offer_link is not None:
            # yield {
            #    'offer_link': offer_link
            # }
            #print(offer_link)
            yield from response.follow_all(offer_link, callback=self.parse_offer)
    
    
    def parse_offer(self, response): # parse offer-listing page, get every seller's link
        items = SellersItem()
        
        # get product url on the page 
        product_url = response.css('#olpDetailPageLink::attr(href)').get()
        
        # generate sellers links
        for url in response.css('.a-text-bold a::attr(href)').getall():
            url = urlparse(url)
            query = url[4].split('&')[1:]
            amazon = 'https://www.amazon.de/sp?_encoding=UTF8&'
            seller_url = amazon + ('&').join(query)

            items['of_seller_link'] = seller_url # seller link on offer-listing page
            items['of_product_link'] = product_url # product link on offer-listing page

            yield items

        yield from response.follow_all(css='li.a-last a', callback=self.parse_offer)
