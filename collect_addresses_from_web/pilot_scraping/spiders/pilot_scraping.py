import scrapy, pandas as pd, numpy as np
from pilot_scraping.items import PilotScrapingItem
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opt = Options()
opt.add_argument('--headless')
class PilotScraping(scrapy.Spider):
    name = 'pilot_scraping'
    ns_list = pd.read_csv('./pilot_info.csv', header=0)
    start_urls = ns_list['url']
    allowed_domains =[ url.replace("https://",'').replace("http://","")  for url in start_urls]
    def parse(self, response):
        #print(response.headers)
        #sel = scrapy.Selector(response)
        #links_in_a_page = sel.xpath('//a[@href]')  # 页面内的所有链接
        item = PilotScrapingItem()
        print(response.url)
        #print(response.url_list)
        # driver = webdriver.Chrome(options=opt)
        # driver.get(response.url)
        for link in response.url_list:
            if link==None:
                continue
            if len(link)<5:
                continue
            # link = str(link_sel.re('href="(.*?)"')[0])  # 每一个url
            # if link:
            #
            #     if not link.startswith('http'):  # 处理相对URL
            #         link = response.url + link
            #     if ":" in link[7:]:
            #         continue
            #     if "///" in link[7:]:
            #         continue
            #     if link.count("?") > 1:
            #         continue
            #     if ".mp4" in link:
            #         continue
            #     if ".mp3" in link:
            #         continue
            #     if link.endswith(".js"):
            #         continue
            yield scrapy.Request(link, callback=self.parse)  # 生成新的请求, 递归回调self.parse
        item['link'] = response.url
        soup = BeautifulSoup(response.text)
        for script in soup(["script", "style"]):
            script.decompose()
        item['link_text'] = soup.get_text()
        item['full_html'] = response.text
        yield item



