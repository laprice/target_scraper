from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from target.items import TargetItem

class TargetSpider(BaseSpider):
    name = "target"
    allowed_domains = ["dailydeals.target.com", "target.com", "www.target.com" ]
    start_urls = [ "http://dailydeals.target.com/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        deals = []
        fdiv = hxs.select("//div[@id='dealsContent']")
        for d in fdiv:
            t = TargetItem()
            t['link'] = d.select(".//p[@class='siteLink']/a/@href").extract().pop()
            t['product'] = d.select(".//p[@class='siteLink']/a/text()").extract().pop()
            t['price'] = d.select(".//div[@class='dealPrice']/p/text()"
                                  ).extract().pop().strip()
            t['list_price'] = d.select(".//p[contains(@class,'lstPrice')]/del/text()"
                                       ).extract().pop().strip()
            deals.append(t)
        tiles = hxs.select("//div[@class='tileInfo']")
        for d in tiles:
            t = TargetItem()
            t['link'] = d.select(".//span[@class='productTitle']/a/@href").extract().pop()
            t['product'] = d.select(".//span[@class='productTitle']/a/@title").extract().pop()
            t['price'] = d.select(".//p[@class='price']/text()").extract().pop().strip()
            t['list_price'] = d.select(".//p[contains(@class,'lstPrice')]/del/text()"
                                       ).extract().pop().strip()
            deals.append(t)
        return deals
