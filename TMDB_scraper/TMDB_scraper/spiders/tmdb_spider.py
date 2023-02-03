# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/438148-minions-the-rise-of-gru?language=en-US']

    def parse(self, response):
        cast_link = response.css('p.new_button a::attr(href)').get()
        cast_link = 'https://www.themoviedb.org/' + cast_link
        if cast_link:
            yield Request(cast_link, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        actor_links = response.css('section.panel.pad:first-child ol.people.credits div.info p a::attr(href)').getall()
        actor_links = ['https://www.themoviedb.org' + link for link in actor_links]
        for link in actor_links:
            yield Request(link, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        for show in response.css('a.tooltip'):
            actor_name = response.css('h2.title a::text').get()
            movie_or_TV_name = show.css('bdi::text').get()

            yield {"actor" : actor_name,
                   "movie_or_TV_name" : movie_or_TV_name}