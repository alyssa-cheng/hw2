# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/125935-abbott-elementary']

    def parse(self, response):
        cast_link = response.css('p.new_button a::attr(href)').get()
        if cast_link:
            yield Request(cast_link, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        actor_links = response.css('div.info a::attr(href)')
        actor_links = ['https://www.themoviedb.org/' + link for link in actor_links]
        for link in actor_links:
            yield Request(link, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css('h2.title a::text')

        for show in response.css('a.tooltip'):
            TV_name = show.css('bdi::text')

        yield {"actor" : actor_name,
               "TV_show" : TV_name}