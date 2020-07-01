# -*- coding: utf-8 -*-
import scrapy

from scrapy_book.items import ScrapyBookItem


class SpiderForXPath(scrapy.Spider):
    name = 'spider_xpath_douban'

    def start_requests(self):
        for a in range(100):
            url = 'https://book.jd.com/booktop/0-0-0.html?category=20002-0-0-0-10001-{}#comfort'.format(a)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        items = []

        for book in response.xpath('/html/body/div[8]/div[2]/div[3]/div[1]/ul[1]/li'):
            item = ScrapyBookItem()
            title1 = book.xpath("div[3]/a/@title").extract_first().replace('\n', '').strip()
            # title2 = "无" if book.xpath("./tr/td[2]/div[1]/span/text()").extract_first() == None else book.xpath(
            #     "./tr/td[2]/div[1]/span/text()").extract_first().replace('\n', '').strip()
            item['title'] = title1 #+ "(" + title2 + ")"
            item['author']=book.xpath("div[3]/dl[1]/dd/a[1]/@title").extract_first().replace('\n', '').strip()
            item['publisher']=book.xpath("div[3]/dl[2]/dd/a[1]/@title").extract_first().replace('\n', '').strip()
            # item['s_img'] = book.xpath("./tr/td[1]/a/img/@src").extract_first().replace('\n', '').strip()
            # item['scrible'] = "无" if book.xpath("./tr/td[2]/p[2]/span/text()").extract_first() == None else book.xpath(
            #     "./tr/td[2]/p[2]/span/text()").extract_first().replace('\n', '').strip()
            sub_url = 'https://'+book.xpath("div[3]/a/@href").extract_first().replace('\n', '').strip()[2:]
            items.append(item)

            #meta={"item":item} #传递item引用SinaItem对象
            yield scrapy.Request(url=sub_url, callback=self.parse_second, meta={"item": item})

    def parse_second(self, response):
        item = response.meta["item"]
        z=response.xpath('/html/body/div[6]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/strong')
        item["category_id"] = "123123123"
        item["category"] = "12313123123"
        # book = response.xpath('//div[@class="indent"]/div').extract_first()
        # item["author"] = book.xpath("./div[1]/a[1]/text()").extract_first().replace('\n', '').strip()
        # item["publisher"] = book.xpath("./div[1]/a/@href").extract_first().replace('\n', '').strip()
        # item["pub_date"] = book.xpath("./div[1]/a/@href").extract_first().replace('\n', '').strip()
        # item["price"] = book.xpath("./div[1]/a/@href").extract_first().replace('\n', '').strip()
        # item["m_img"] = book.xpath("./div[1]/a/@href").extract_first().replace('\n', '').strip()
        # item["b_img"] = book.xpath("./div[1]/a/@href").extract_first().replace('\n', '').strip()
        # item["isbn"] = book.xpath("./div[2]/a[1]/text()").extract_first().replace('\n', '').strip()
        yield item