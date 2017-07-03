# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteasymusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    singer_id = scrapy.Field()
    singer_name = scrapy.Field()
    album_id = scrapy.Field()
    album_name = scrapy.Field()
    songs_num = scrapy.Field()
    release_date = scrapy.Field()
    sharings_num = scrapy.Field()
    reviews_num = scrapy.Field()
