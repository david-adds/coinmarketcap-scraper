import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoinsSpider(CrawlSpider):
    name = 'coins'
    
    user_agent = 'Mozilla/5.0 (Linux; Android 12; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.70 Mobile Safari/537.36'
    
    def start_requests(self):
        yield scrapy.Request(url='https://coinmarketcap.com', headers={
            'User-Agent': self.user_agent
        })
        
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='cmc-link']"), callback='parse_item', follow=True, process_request='set_user_agent')
    )       

    def set_user_agent(self,request,spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    

    def parse_item(self, response):
        yield {
            'name': response.xpath("normalize-space(//div[@class='n78udj-3 emihhf popped']/span/b/text())").get()
            # 'rank': response.xpath("//div[@class='namePill namePillPrimary']/text()").get(),
            # 'price(USD)': response.xpath("//div[@class='priceValue ']/span/text()").get()
        }

