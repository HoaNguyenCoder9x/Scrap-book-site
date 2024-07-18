from typing import Any
import scrapy
from scrapy.http import Response
from tutorial.items import BookDetail
from datetime import datetime

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
   
    # custom_settings = {
    #         'FEEDS': { 'data.csv': { 'format': 'csv',}}
    #         }
    
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_link = book.css('h3 a::attr(href)').get()
            #call to func to parse data
            yield response.follow(relative_link, callback=self.parse_book_details) 
            

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     #Call next page
        #     yield response.follow(next_page, callback=self.parse)

    # parse data detail
    def parse_book_details(self, response: Response, **kwargs: Any) -> Any:
        book_details = BookDetail()
        
        
        book_details['title'] = response.css('h1::text').get(),
        book_details['price'] =  response.css('p.price_color::text').get()

        book_details['description'] = response.css('#product_description+ p::text').get(),
        book_details['cateogry']= response.css('li~ li+ li a::text').get(),
        book_details['availability'] = response.css('table.table td::text')[5].get(),
        book_details['upc'] = response.css('table.table td::text')[0].get(),
        book_details['rating'] = response.css('p.star-rating::attr(class)').get()
        book_details['last_updated_dt'] = datetime.now()
        yield book_details

            
        
        
         
        

        
        
