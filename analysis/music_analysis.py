import pymysql
import pandas as pd
import numpy as np
import json

#读取数据
conn = pymysql.connect(host='127.0.0.1',user='root',passwd='charrychen',db='scraping')
music_df = pd.read_sql('SELECT * FROM songs',con=conn)

#转换数据类型
music_df['singer_id'] = music_df['singer_id'].astype(np.int)
music_df['songs_num'] = music_df['songs_num'].astype(np.int)
music_df['release_date'] = pd.to_datetime(music_df['release_date'])
music_df['sharings_num'] = music_df['sharings_num'].astype(np.int)
music_df['reviews_num'] = music_df['reviews_num'].astype(np.int)

#每个歌手的专辑总数
group = music_df['album_id'].groupby(music_df['singer_id'])
singer_df = pd.DataFrame() #创建歌手表
singer_df['singer_id'] = group.count().index #添加歌手id到歌手表
singer_name_map = dict ()  #构建歌手id和歌手姓名映射
for i in range(music_df.shape[0]):
    key = music_df.ix[i,'singer_id']
    value = music_df.ix[i,'singer_name']
    singer_name_map[key] = value
singer_df['singer_name'] = singer_df['singer_id'].map(singer_name_map) #添加歌手姓名列
singer_df['albums_num'] = group.count().values #添加每个歌手的专辑总数列
#每个歌手的歌曲总数
group = music_df['songs_num'].groupby(music_df['singer_id'])
singer_df['songs_num'] = group.sum().values
#每个歌手分享总数分布
group = music_df['sharings_num'].groupby(music_df['singer_id'])
singer_df['sharings_num'] = group.sum().values
#每个歌手评论总数分布
group = music_df['reviews_num'].groupby(music_df['singer_id'])
singer_df['reviews_num'] = group.sum().values
output = singer_df.to_json(orient='split') #保存为json文件
with open('./output/singer_df.json','wb') as f:
    f.write(output.encode('utf-8'))
#每张专辑包含的歌曲数量分布
album_df = pd.DataFrame()
album_df['album_id'] = music_df['album_id']
album_df['album_name'] = music_df['album_name']
album_df['songs_num'] = music_df['songs_num']
#每张专辑分享数量分布
album_df['sharings_num'] = music_df['sharings_num']
#每张专辑评论数量分布
album_df['reviews_num'] = music_df['reviews_num']
#将每张专辑发布时间精度改为年份，添加新列
music_df['release_year'] = music_df['release_date'].apply(lambda x: x.year)
album_df['release_year'] = music_df['release_year'] #添加专辑发布年份
music_df.to_json('./output/music_df.json',orient='split') #保存为json文件
album_df.to_json('./output/album_df.json',orient='split')
#生成echart散点图需要的数据格式 [x,y,size]
cols = list(album_df)
cols.insert(0,cols.pop(cols.index('sharings_num')))
cols.insert(1,cols.pop(cols.index('reviews_num')))
cols.insert(2,cols.pop(cols.index('songs_num')))
cols.insert(3,cols.pop(cols.index('release_year')))
cols.insert(4,cols.pop(cols.index('album_name')))
cols.insert(5,cols.pop(cols.index('album_id')))
album_df2 = album_df.ix[:,cols]
album_df2.to_json('./output/album_df2.json',orient='split')
#按年份统计专辑数量
group = music_df['album_id'].groupby(music_df['release_year'])
years = group.count()
years.drop([2046],axis=0,inplace=True)
years.to_json('./output/years.json',orient='split')
#分享数最高的专辑
music_df.sort_values(by='sharings_num',ascending=False).iloc[0:9,]
#评论数最高的专辑
music_df.sort_values(by='reviews_num',ascending=False).iloc[0:9,]
#歌曲数量最多的专辑
music_df.sort_values(by='songs_num',ascending=False).iloc[0:9,]

#分享总数最高的歌手
singer_df.sort_values(by='sharings_num',ascending=False).iloc[0:9,]
#评论总数最高的歌手
singer_df.sort_values(by='reviews_num',ascending=False).iloc[0:9,]
#发布歌曲最多的歌手
singer_df.sort_values(by='songs_num',ascending=False).iloc[0:9,]
