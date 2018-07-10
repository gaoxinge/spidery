# -*- coding: utf-8 -*-
"""
url: https://movie.douban.com/tag/2016
fetch: requests
parse: lxml
presist: txt
"""
import requests
from lxml import etree
from spidery import Spider

spider = Spider(
    urls = ['https://movie.douban.com/tag/2016?start=' + str((i-1)*20) for i in range(1, 10)],
)

@spider.fetch
def fetch(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return response

@spider.parse
def parse(response):
    root = etree.HTML(response.text)
    results = root.xpath('//div[@class=\'pl2\']')
    for result in results:
        movie = {}
        movie['title']  = result.xpath('a/text()')[0][:-2].strip()
        movie['rating'] = float(result.xpath('.//span[@class=\'rating_nums\']/text()')[0])
        movie['vote']   = int(result.xpath('.//span[@class=\'pl\']/text()')[0][1:][:-4])
        yield movie, None
        
@spider.presist
def presist(item):
    f.write(str(item) + '\n')

f = open('douban.txt', 'wb')
spider.consume_all()
f.close()