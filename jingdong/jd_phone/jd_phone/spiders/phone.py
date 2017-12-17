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
    bash_url = "https://search.jd.com/Search?keyword=手机&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&cid2=653&cid3=655&click=0"
    barnds_list = []
    barnds_file = "/Users/yangxuan/code/crawler/scrapy/example/jingdong/jd_phone/input_data/brands"

    def start_requests(self):
        #请求第一页，无需渲染js
        self.initBrands()
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
            meta = {'page':i}
            yield SplashRequest(url,
                            endpoint='execute',
                            args={'lua_source':lua_script},
                            cache_args=['lua_source'],
                            meta = meta)


    def parse(self, response):
        sale_rank = 0
        for sel in response.css('ul.gl-warp.clearfix > li.gl-item'):
            sale_rank = sale_rank + 1
            pid = sel.xpath('@data-pid').extract_first()
            name = sel.css('div.p-name em::text').extract_first()
            page = response.meta['page']
            # 通过request传递过来的page计算出销量排行
            yield {
            'name':name,
            'pid':pid,
            'price':sel.css('div.p-price i::text').extract_first(),
            'brand':self.getBrand(name),
            'sale_rank':page*60+sale_rank,
            'comment':sel.css('div.p-commit strong a::text').extract_first(),
            'shop':sel.css('div.p-shop a::text').extract_first(),
            'icons':sel.css('div.p-icons i::text').extract_first(),
            'href':"https://item.jd.com/" + pid +".html",
        	}

    def initBrands(self):
        with open(self.barnds_file) as brands:
            self.barnds_list = brands.readlines()
        #for line in self.barnds_list:
            #print(line.rstrip())

    def getBrand(self,text):
        print (text)
        for line in self.barnds_list:
            if text.lower().find(line.strip().lower()) > -1:
                return line.rstrip()
        return "其他"

            




