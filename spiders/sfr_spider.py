# coding: utf-8
from scrapy import Spider, Request, Selector
from scrapy.item import Item, Field
from scrapy.http import Request, FormRequest
import re, os
from items import AirbnbItem, SfrItem
import json

# text = u"hello, j'ai une couille\u2014"
# print(text.encode('utf-8'))
# text = u'Comment modifier vos coordonn\xe9es en ligne ?'
# print(text.encode('utf-8'))

def remove_tabs(text):
    text = text.replace('\t', '')
    return text

def remove_returns(text):
    text = text.replace('\n\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    text = text.strip()
    return text


class sfr(Spider):
    name = "sfr"
    # allowed_domains = ["http://communaute.red-by-sfr.fr"]

    start_urls = [
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/2",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/3",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/4",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/5",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/6",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/7",
        "http://communaute.red-by-sfr.fr/t5/FAQ/tkb-p/FAQ/page/8"
    ]

    os.remove('sfr.json')

    def parse(self, response):
        urls = []
        for href in response.css(".subject_col > a::attr('href')").extract():
            urls.append(response.urljoin(href))
        for url in urls:
            yield Request(url, callback=self.parse_content, dont_filter=True)


    def parse_content(self, response):

        title = response.xpath('//div[@class="article_title"]//h1/text()').extract()[0]
        question = response.xpath('//div[@class="lia-message-template-content-zone"]//h2/text()').extract()
        answer = response.xpath('//div[@class="lia-message-template-content-zone"]').extract()
        # for i in range(len(answer)):
        #     answer[i] = remove_tabs(remove_returns(remove_tags(answer[i]))).encode('utf-8')
        for i in range(len(question)):
            question[i] = remove_returns(question[i]).encode('utf-8')
        image = response.xpath('//div[@class="lia-message-template-content-zone"]//@src').extract()
        link = response.xpath('//div[@class="lia-message-template-content-zone"]//@href').extract()
        item = SfrItem()
        item["url"] = response.url
        item["title"] = title.encode('utf-8')
        item["question"] = question
        item["answer"] = answer
        item["image"] = image
        item["link"] = link
        yield item
        # with open("sfr.json", 'w+') as f:
        #     json.dump(dict(item), f, indent=4)
