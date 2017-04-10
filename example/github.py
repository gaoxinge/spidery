# -*- coding: utf-8 -*-
"""
url:   https://github.com
http:  requests
parse: lxml
"""
import requests
from lxml import etree
from collections import defaultdict
from spidery import Spider

spider = Spider(
    urls   = ['https://github.com/gaoxinge?tab=following'],
    filter = set(['https://github.com/gaoxinge?tab=following']),
)

@spider.http
def http(url):
    spider.log('http', 'start', url)
    response = requests.get(url)
    spider.log('http', 'end', url)
    return response
    
@spider.parse
def parse(response):
    root = etree.HTML(response.text)
    results = root.xpath('//span[@class=\'link-gray pl-1\']/text()')
    name = response.url[19:][:-14]
    spider.log('parse', 'ok', '\n\n{' + name + ': ' + str(results) + '}\n')
    for result in results:
        spider.lock.acquire()
        d[name].append(result)
        spider.lock.release()
        tmp = 'https://github.com/' + result + '?tab=following'
        spider.add(tmp)

d = defaultdict(list)
spider.run(3)