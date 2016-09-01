# coding: utf-8
from scrapy import Spider, Request, Selector
from scrapy.item import Item, Field
from scrapy.http import Request, FormRequest
import re
from items import AirbnbItem
import json, urllib

text = u"hello, j'ai une couille\u2014"
print(text.encode('utf-8'))
text = '\xe2\x80\x99'
print(text.decode('utf-8').encode('utf-8'))

def remove_tags(text):
    return re.sub(r'<.*?>', '', text)

def remove_tabs(text):
    text = text.replace('\t', '')
    return text

def remove_returns(text):
    text = text.replace('\n\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    text = text.strip()
    return text

sentence = "J'auré aimai manger"


class google(Spider):
    name = "google"
    allowed_domains = ["google.fr"]

    start_urls = [
        "www.google.fr/search?q=" + urllib.quote_plus(sentence)
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="med"]/div/p/a/text()').extract():
            print(href)
