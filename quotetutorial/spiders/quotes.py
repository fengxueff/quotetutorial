# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    #通过命令行模式scrapy shell quotes.toscrape.com也能进入到parse这个方法体中
    #方便调式
    def parse(self, response):
        # print(response.text)
        #获取标签
        quotes = response.css(".quote")
        for quote in quotes:
            # 获取class=text标签中的文本内容，取第一行
            text = quote.css(".text::text").extract_first()
            author = quote.css(".author::text").extract_first()
            #获取class=tags下的class=tag的文本内容，取所有数据
            tags = quote.css(".tags .tag::text").extract()

            item = QuoteItem()
            #这个地方居然不能支持对象点属性的方式来调用
            item["text"] = text
            item["author"] = author
            item["tags"] = tags
            #当使用yield后scrapy就会默认的解析这个item
            #yield只适用于item类与request类
            #通过 scrapy crawl quotes -o quotes.json 就可以将item保存在json文件中了
            #而通过scrapy crawl quotes -o quotes.csv就可以将item保存为csv文件
            # 而通过scrapy crawl quotes -o quotes.xml就可以将item保存为xml文件
            #也可以将目标文件保存在ftp中，如：ftp://user:pass@ftp.exsample.com/path/quotes.xml
            yield item
        #获取下一页按钮对应的url值
        next = response.css(".pager .next a::attr(href)").extract_first()
        #将next获得的相对url=/page/2/转换成绝对url
        url =  response.urljoin(next)
        #发起一个请求，用于获取下一页，然后递归调用parse方法来解析网页内容
        yield scrapy.Request(url=url,callback=self.parse)
