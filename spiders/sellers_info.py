# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os.path
from os import path
from ..items import AmazonSellersItem

class SellersInfoSpider(scrapy.Spider):
    name = 'sellers_info'

    urls = []
    if path.exists("sellers.csv"):
    
        df = pd.read_csv('sellers.csv')
        #df.drop_duplicates(keep='first', inplace=True)
        urls = df['seller_link'].tolist()
        
    start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, callback=self.parse)

    def parse(self, response):   
        items = AmazonSellersItem()

        items['seller_name'] = response.css('#storefront-link .a-link-normal::text').get()  
        items['biz_name'] = response.xpath("//span[contains(., 'Geschäftsname:')]/../text()").get()
        items['biz_type'] = response.xpath("//span[contains(., 'Geschäftsart:')]/../text()").get()
        items['rating_star'] = response.css('.feedback-detail-stars *::text').get()
        items['rating'] = response.xpath("string(//a[@class='a-link-normal feedback-detail-description'][1])").getall()
        items['biz_address'] = ','.join(response.xpath("//span[contains(., 'Geschäftsadresse:')]/following-sibling::\
                               ul//text()").getall())
        items['customer_service_address'] = ','.join(response.xpath("//span[contains(., 'Kundendienstadresse:')]\
                                            /following-sibling::ul//text()").getall())
        items['phone'] = response.xpath("//span[contains(., 'Telefonnummer:')]/../text()").get()
        items['email'] = response.xpath("//div[@id='about-seller']//text()[contains(.,'@')]").get()
        items['seller_link'] = response.url
        items['marketplace'] = response.css('#storefront-link .a-link-normal::attr(href)').get()
        
        yield(items)
