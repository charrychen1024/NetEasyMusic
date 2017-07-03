# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class NeteasymusicPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='charrychen',db='scraping',charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        singer_id = item['singer_id']
        singer_name = item['singer_name']
        album_id = item['album_id']
        album_name = item['album_name']
        songs_num = item['songs_num']
        release_date = item['release_date']
        sharings_num = str(item['sharings_num'])
        reviews_num = str(item['reviews_num'])

        #sql = "INSERT INTO songs VALUES('"+singer_id+"', '"+singer_name+"', '"+album_id+"', '"+album_name+"', '"+songs_num+"', '"+release_date+"', '"+sharings_num+"', '"+reviews_num+"')"
        sql = "INSERT INTO songs VALUES('"+singer_id+"', '"+singer_name+"', '"+album_id+"', '"+album_name+"', '"+songs_num+"', '"+release_date+"', '"+sharings_num+"', '"+reviews_num+"')"
        #sql = "INSERT INTO songs(singer_id,singer_name,album_id,album_name,songs_num,release_date,sharings_num,reviews_num) VALUES('1','1','1','1','1','1','1','1')"
        self.cur.execute(sql)
        self.conn.commit()

        return item

    def close_spider(self,spider):
        #self.cur.close()
        self.conn.close()
