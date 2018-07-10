# -*- coding: utf-8 -*-
"""
url: https://github.com
fetch: requests
parse: lxml
presist: print
"""
import requests
from lxml import etree
from spidery import Spider

spider = Spider(
    urls = ['https://github.com/gaoxinge?tab=following'],
)

@spider.fetch
def fetch(url):
    response = requests.get(url)
    return response
    
@spider.parse
def parse(response):
    root = etree.HTML(response.text)
    results = root.xpath('//span[@class=\'link-gray pl-1\']/text()')
    name = response.url[19:][:-14]
    for result in results:
        relation = {}
        relation['name'] = name
        relation['result'] = result
        url = 'https://github.com/' + result + '?tab=following'
        yield relation, [url]
        
@spider.presist
def presist(item):
    print item['name'], item['result']

spider.consume_all()