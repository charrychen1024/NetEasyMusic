# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from neteasymusic.items import NeteasymusicItem
import urllib.request
#import requests

class MusicspiderSpider(scrapy.Spider):
    name = 'musicspider'
    allowed_domains = ['music.163.com']
    #host = 'http://music.163.com'
    start_singer_id = 2001 #设置起始歌手id
    start_urls = 'http://music.163.com/artist/album?id='+str(start_singer_id)
    def start_requests(self):
        yield Request(self.start_urls, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'})

    def parse(self, response):
        item = NeteasymusicItem()
        singer_id = response.url[response.url.index('=')+1:] #获取歌手id
        try:
            singer_name = response.xpath("//h2[@id='artist-name']/text()").extract()[0]
        except:
            print('Not found page - '+response.url)
            singer_name = 'Error, not found'
        #singer_name = 'abc'
        if singer_name != 'Error, not found': #只有找到对应网页时才进行后续数据提取操作，否则直接爬取下一个网页

            #获取专辑列表网页
            try:
                ab_pages_num = int(response.xpath("//div[@class='u-page']/a/text()").extract()[-2])
            except:
                ab_pages_num = 1
            #print(ab_pages_num)
            #获取每个专辑的url
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36")]
            urllib.request.install_opener(opener)

            albums_url = []
            for i in range(ab_pages_num):
                albums_page = 'http://music.163.com/artist/album?id='+singer_id+'&limit=12&offset=%d' % (i*12)
                print('albums_page: ' + albums_page)
                data_albums = urllib.request.urlopen(albums_page).read().decode('utf-8')
                #data_albums = requests.get(album_page)
                #sel = scrapy.Selector(data_albums)
                #albums_url.append(sel.xpath("//ul[@id='m-song-module']/li/div/a[@class='msk']/@href"))
                pat_url = '<a href="(.*?)" class="msk">'
                albums_url.append(re.compile(pat_url).findall(data_albums))
                #print(albums_url)

            for i in range(ab_pages_num):
                for j in albums_url[i]:
                    data_per_album = urllib.request.urlopen('http://music.163.com' + j).read().decode('utf-8')
                    print('album_page: ' + 'http://music.163.com' + j)
                    #sel = scrapy.Selector(data_per_album)
                    item['singer_id'] = singer_id
                    print('singer_id = '+singer_id)
                    item['singer_name'] = singer_name
                    print('singer_name = '+singer_name)
                    album_id = singer_id + "_" + re.sub("\D","",j)
                    item['album_id'] = album_id
                    print('album_id = '+album_id)
                    pat_album_name = '<h2 class="f-ff2">(.*?)</h2>'
                    album_name = re.compile(pat_album_name).findall(data_per_album)[0]
                    item['album_name'] = album_name
                    print('album_name = '+album_name)
                    pat_songs_num = '<span class="sub s-fc3">(.*?)</span>'
                    songs_num = re.compile(pat_songs_num).findall(data_per_album)[0].replace('首歌','')
                    item['songs_num'] = songs_num
                    print('songs_num = '+songs_num)
                    pat_release_date = '发行时间：</b>(.*?)</p>'
                    release_date = re.compile(pat_release_date).findall(data_per_album)[0]
                    item['release_date'] = release_date
                    print('release date = '+release_date)
                    pat_sharings_num = 'href="javascript:;"><i>(.*?)</i></a>'
                    sharings_num = re.compile(pat_sharings_num).findall(data_per_album)[0]
                    if sharings_num == '分享':
                        sharings_num = 0
                    else:
                        sharings_num = sharings_num.replace('(','').replace(')','')
                    item['sharings_num'] = sharings_num
                    print('sharings_num = '+str(sharings_num))
                    pat_reviews_num = '<span id="cnt_comment_count">(.*?)</span>'
                    reviews_num = re.compile(pat_reviews_num).findall(data_per_album)[0]
                    if reviews_num == '评论':
                        reviews_num = 0
                    item['reviews_num'] = reviews_num
                    print('reviews_num = '+str(reviews_num))
                    #item['album_name'] = sel.xpath("//div[@class='tit']/h2/text()").extract()
                    #songs_num = sel.xpath("//span[@clss='sub s-fc3']/text()").extract()
                    #item['songs_num'] = songs_num.replace("首歌","")
                    #item['release_date'] = sel.xpath("//div[@class='topblk']/p[2]/text()").extract()
                    #item['sharings_num'] = sel.xpath("//div[@id='content-operation']/a[4]/text()").extract()
                    #item['reviews_num'] = sel.xpath("//span[@id='cnt_comment_count']/text()").extract()
                    yield item #生成item
        #爬取下一位歌手
        singers_num = 10000
        for i in range(self.start_singer_id+1,self.start_singer_id+singers_num+1):
            next_singer_url = 'http://music.163.com/artist/album?id=' + str(i)
            yield Request(next_singer_url,callback=self.parse,headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'})












