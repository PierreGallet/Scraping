# Scraping with scrapy

## How to

* select the item fields you nedd in item.py
* create your spider, mostly modifying the the *response.css* and *response.xpath* commands.
* use `scrapy crawl name_of_your_spider -o output.json` to lauch the crawling and save the result in a json format.
