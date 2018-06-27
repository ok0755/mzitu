# coding:utf-8
import requests
from lxml import html
import os
import time
import fake_useragent
import random
import multiprocessing
from gevent import monkey,pool
monkey.patch_socket()
import gevent

def header(referer):
    agents=fake_useragent.UserAgent()
    agent=agents.random
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': agent,
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers

# 获取主页列表
def getPage(pageNum):
    time.sleep(1)
    urls=[]
    baseUrl='http://www.mzitu.com/page/{}/'.format(pageNum)
    selector=html.fromstring(requests.get(baseUrl).content)
    for ur in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(ur)
    return urls

def getPiclink(url):
    gevent.sleep(3)
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    n=1
    for i in range(int(total)):
        try:
            link = '{}/{}'.format(url, i+1)
            s = html.fromstring(requests.get(link).content)
            jpgLink = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            print jpgLink
            filename = 'd:\\mzitu\\{}.jpg'.format(int(time.time()*10))
            with open(filename, "wb+") as jpg:
                jpg.write(requests.get(jpgLink, headers=header(jpgLink)).content)
            n+= 1
        except:
            pass

if __name__ == '__main__':
    p=pool.Pool(20)
    pageNum=input(u'Enter page:>>> ')
    page=getPage(pageNum)
    th=[]
    for pic_url in page:
        th.append(p.spawn(getPiclink,pic_url))
    gevent.joinall(th)
'''
    p=multiprocessing.Pool(processes=4)
    for pic_url in page:
        p.apply_async(getPiclink,(pic_url,))
    p.close()
    p.join()
'''
