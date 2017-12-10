# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

class SoimageSpider(scrapy.Spider):

    BASE_URL = 'http://images.so.com/zj?ch=beauty&sn=%s&listtype=new&temp=1'
    start_index = 0

    #最大下载数量
    MAX_DOWLOAD_NUM = 1000

    name = 'soImage'
    start_urls = [BASE_URL%0]

    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))

        #提取所有图片下载url到一个列表，赋给item的image_url 字段
        yield {'image_urls':[info['qhimg_url'] for info in infos['list']]}

        self.start_index += infos['count']

        if infos['count'] > 0 and self.start_index < self.MAX_DOWLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index)