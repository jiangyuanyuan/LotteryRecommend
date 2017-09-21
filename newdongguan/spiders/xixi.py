# -*- coding: utf-8 -*-
import scrapy
from newdongguan.items import NewdongguanItem


class DongdongSpider(scrapy.Spider):
    name = 'hehe'

    allowed_domains = ['www.gdtai.com']

    url = 'http://www.gdtai.com/info/ssq_1/'
    offset = 1
    start_urls = [url]
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    cookie = "Hm_lvt_a7c208b1d88d264468dc5a1c4ea808e6=1505654114,1505690668,1505964849; Hm_lpvt_a7c208b1d88d264468dc5a1c4ea808e6=1505965383"  # 带着Cookie向网页发请求\
    # cookie = "Hm_lpvt_a7c208b1d88d264468dc5a1c4ea808e6	1505978145"  # 带着Cookie向网页发请求\
    #
    # def start_requests(self):
    #     yield scrapy.Request(url=self.start_urls[0], headers = self.headers, cookies=self.cookie)  # 这里带着cookie发出请求

    def parse(self, response):
        # 每一页里的所有帖子的链接集合
        # links = response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract()
        links1 = response.xpath('//div[@class = "info_comtent_li"]//a/@href').extract()
        # links2 = response.xpath('//div[@class="content"]//div[@class="zx_lbor"]//a/@href').extract()
        links = links1
        # 迭代取出集合里的链接
        for link in links:
            if link != '':
                # 提取列表里每个帖子的链接，发送请求放到请求队列里,并调用self.parse_item来处理
                # ../../xinwen/caizhongxinwen-ssq/500159.shtml
                # 2017 / 0525 / 4840070.html
                # if "../.." in link:
                #     link = link.replace("../..","")
                print link
                # if "http://www.cjcp.com.cn" in link:
                yield scrapy.Request(link, callback = self.parse_item)
                # elif "html" in link:
                #     yield scrapy.Request("http://www.cjcp.com.cn/"+link, callback = self.parse_item)
                # else:
                #     yield scrapy.Request("http://www.cjcp.com.cn/"+link+".html", callback = self.parse_item)


        # 页面终止条件成立前，会一直自增offset的值，并发送新的页面请求，调用parse方法处理
        if self.offset <= 800:
            self.offset += 1
            # 发送请求放到请求队列里，调用self.parse处理response
            # http: // www.gdtai.com / info / ssq_3 /
            yield scrapy.Request("http://www.gdtai.com/info/ssq_" +str(self.offset)+"/", callback = self.parse)

    # 处理每个帖子的response内容
    def parse_item(self, response):
        # try:
        item = NewdongguanItem()

        # 标题
        # item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        item['title'] = response.xpath('//div[@class = "article_cent"]//h1/text()').extract()[0]
        # 编号
        item['time'] = response.xpath('//div[@class = "article_cent"]//span/text()').extract()[0]
        # time2= response.xpath('//div[@class="content"]//div[@class="zx_all"]/text()').extract()[0]
        # item['time'] = time1 =time2
        #  = str(time).replace("&nbsp","")
        # 内容，先使用有图片情况下的匹配规则，如果有内容，返回所有内容的列表集合
        contents = response.xpath('//div[@class = "article_cent"]//p/text()').extract()
        # contentsp = response.xpath('//div[@class="content"]//div[@class="font14"]//p/text()').extract()
        # contentsdiv = response.xpath('//div[@class="content"]//div[@class="font14"]/text()').extract()
        # contentsstrong= response.xpath('//div[@class="content"]//div[@class="font14"]//strong/text()').extract()

        content =""
        # for condiv in contentsdiv:
        #     content = content + condiv
        # for constp in contentsp:
        #     content = content + constp
        # for constrong in contentsstrong:
        #     content = content + constrong
        for cont in contents:
            print cont
            content = content+"/r/n"+cont

        # item['content']= str(content).replace(" ", "")
        item['content']= content
        # item['content']= str(content).replace("&nbsp","")

        item['url'] = response.url
        # except Exception, e:
        #     print "parse_item failue"

        # 交给管道
        yield item

