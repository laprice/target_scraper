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
            t['link'] = d.select(".//p[@class='siteLink']/a/@href").extract()
            t['product'] = d.select(".//p[@class='siteLink']/a/text()").extract()
            t['price'] = d.select(".//p[@class='dealPrice']/text()").extract()
            t['list_price'] = d.select(".//p[@class='originalPrice']/del/text()"
                                       ).extract()
            deals.append(t)
        tiles = hxs.select("//div[@class='tileInfo']")
        for d in tiles:
            t = TargetItem()
            t['link'] = d.select(".//p[@class='productTitle']/a/@href").extract()
            t['product'] = d.select(".//p[@class='productTitle']/a/@title").extract()
            t['price'] = d.select(".//p[@class='price']/text()").extract()
            t['list_price'] = d.select(".//p[@class='listPrice']/del/text()"
                                       ).extract()
            deals.append(t)
        return deals
