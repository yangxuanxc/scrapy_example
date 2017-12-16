# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash)
	splash:go(splash.args.url)
	splash:wait(2)
	splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
	splash:wait(2)
	return splash:html()
end
'''
#先起服务.然后配置文件。
class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['search.jd.com']
    bash_url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&pvid=e8b433568f0f43b680004810c674011e"

    def start_requests(self):
        #请求第一页，无需渲染js
        yield Request(self.bash_url, callback = self.parse_urls, dont_filter = True)

    def parse_urls(self,response):
        #获取商品总数，计算出总页数
        #total = int(response.css('span#J_resCount::text').extract_first())
        #pageNum = total // 60 + (1 if total % 60 else 0)
        #total = 2
        pageNum = 100

        # 构造每页的url，向Splash的execute断点发送请求
        for i in range(pageNum):
     	    url ='%s&page=%s'%(self.bash_url,2 * i + 1)
     	    yield SplashRequest(url,
     						endpoint='execute',
     						args={'lua_source':lua_script},
     						cache_args=['lua_source'])


    def parse(self, response):
        
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):
        	yield {
        	'name':sel.css('div.p-name em::text').extract_first(),
        	'price':sel.css('div.p-price i::text').extract_first(),
            'comment':sel.css('div.p-commit strong a::text').extract_first(),
            'shop':sel.css('div.p-shop a::text').extract_first(),
            'icons':sel.css('div.p-icons i::text').extract_first(),

        	}
