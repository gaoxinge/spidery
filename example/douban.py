# -*- coding: utf-8 -*-
import requests
from lxml import etree
from spidery import Spider, Item

spider = Spider(
    urls = ['https://movie.douban.com/tag/2016?start=' + str((i-1)*20) for i in range(1, 10)],
)

@spider.http
def http(url):
    spider.log('http', 'start', url)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    spider.log('http', 'end', url)
    return response

@spider.parse
def parse(response):
    Movie = Item('Movie', ['title', 'rating', 'vote'])
    root = etree.HTML(response.text)
    results = root.xpath('//div[@class=\'pl2\']')
    for result in results:
        movie = Movie()
        movie['title']  = result.xpath('a/text()')[0][:-2].strip()
        movie['rating'] = float(result.xpath('.//span[@class=\'rating_nums\']/text()')[0])
        movie['vote']   = int(result.xpath('.//span[@class=\'pl\']/text()')[0][1:][:-4])
        yield movie
        
@spider.save
def save(item):
    f.write(str(item) + '\n')

f = open('douban.txt', 'wb')
spider.run(3)
f.close()