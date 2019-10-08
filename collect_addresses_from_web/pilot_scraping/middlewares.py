# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opt = Options()
opt.add_argument('--headless')
driver = webdriver.Chrome(options=opt,service_args =['--ignore-ssl-errors = true','--load-images=no','--disk-cache=true'])
# driver.set_page_load_timeout(0.1)
# driver.set_script_timeout(0.1)
#driver.implicitly_wait(5)
drive_count=0
#
from scrapy import signals

class PilotScrapingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PilotScrapingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        global driver
        global drive_count
        try:
            print(request.url)
            driver.get(request.url)
        except:
            driver.execute_script('window.stop()')
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//p[@data-a-target='carousel-broadcaster-displayname']"))
        # )
        url_list = [i.get_attribute("href") for i in driver.find_elements_by_tag_name("a")]
        # driver.execute_script('window.stop()')
        body = driver.page_source
        resp = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        resp.url_list = url_list
        drive_count += 1
        if drive_count == 100:
            driver.quit()
            driver = webdriver.Chrome(options=opt, service_args=['--ignore-ssl-errors = true'])
            # driver.set_page_load_timeout(0.1)
            # driver.set_script_timeout(0.1)
            # driver.implicitly_wait(60)
            drive_count = 0
            # har = json.loads(driver.get_log('har')[0]['message'])
        return resp

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
