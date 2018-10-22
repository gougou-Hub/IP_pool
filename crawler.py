import requests
from pyquery import  PyQuery as pq
import json

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=50):
        '''
        获取代理66
        :param page_count: 页码
        :return: 代理
        '''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = requests.get(url).text
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    # def crawl_xdaili(self):
    #     '''
    #     获取讯代理
    #     :return:  代理
    #     '''
    #     url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=7c13caebe8c7483f954b416920f801a2&orderno=YZ201810615663hQTuz&returnType=2&count=20'
    #     html = requests.get(url).text
    #     if html:
    #         result = json.loads(html)
    #         proxies = result.get('RESULT')
    #         for proxy in proxies:
    #             yield proxy.get('ip') + ':' + proxy.get('port')