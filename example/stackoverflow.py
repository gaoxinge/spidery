# -*- coding: utf-8 -*-
"""
url: https://stackoverflow.com/questions
fetch: requests
parse: lxml
presist: txt
"""
import requests
from lxml import etree
from spidery import Spider

spider = Spider(
    urls = ['http://stackoverflow.com/questions/?page=' + str(i) + '&sort=votes' for i in range(1, 4)],
)

@spider.fetch
def fetch(url):
    response = requests.get(url)
    return response

@spider.parse
def parse(response):
    root = etree.HTML(response.text)
    results = root.xpath('//div[@class=\'question-summary\']')
    for result in results:
        question = {}
        question['votes']   = result.xpath('div[@class=\'statscontainer\']//strong/text()')[0]
        question['answers'] = result.xpath('div[@class=\'statscontainer\']//strong/text()')[1]
        question['views']   = result.xpath('div[@class=\'statscontainer\']/div[@class=\'views supernova\']/text()')[0].strip()
        question['title']   = result.xpath('div[@class=\'summary\']/h3/a/text()')[0]
        question['link']    = result.xpath('div[@class=\'summary\']/h3/a/@href')[0]
        yield question, None

@spider.presist
def presist(item):
    f.write(str(item) + '\n')

f = open('stackoverflow.txt', 'wb')
spider.consume_all()
f.close()