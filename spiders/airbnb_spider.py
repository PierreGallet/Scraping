# coding: utf-8
from scrapy import Spider, Request, Selector
from scrapy.item import Item, Field
from scrapy.http import Request, FormRequest
import re
from items import AirbnbItem
import json

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


class airbnb(Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com"]

    start_urls = [
        "https://www.airbnb.com/help/",
    ]

    def parse(self, response):
        urls = []
        for href in response.css(".navtree-list > li > a::attr('href')").extract():
            if (href not in ["#", "/help/contact_us", "/help/feedback", "/help/getting-started/how-it-works", "/help/getting-started/how-to-travel", "/help/getting-started/how-to-host"]):
                urls.append(response.urljoin(href))
        print(urls)
        for url in urls:
            yield Request(url, callback=self.parse_topic)

    def parse_topic(self, response):
        urls = []
        for href in response.css(".help-content > a::attr('href')").extract():
            urls.append(response.urljoin(href))
        print(urls)
        for url in urls:
            print("done for ", url)
            yield Request(url, callback=self.parse_content)


    def parse_content(self, response):

        question = response.xpath('//div[@class="space-8"]/h2/text()').extract()[0].encode('unicode_escape')
        answer = remove_tags(response.xpath('//div[@class="text-copy space-8"]').extract()[0].encode('unicode_escape'))
        answer = remove_tabs(remove_returns(answer))
        print('###############', question, answer)
        print(type(question), type(answer))
        item = AirbnbItem()
        item["question"] = question.encode('utf-8')
        item["answer"] = answer.encode('utf-8')
        yield item
        # with open("airbnb.json", 'w+') as f:
        #     json.dump(str(item), f)
