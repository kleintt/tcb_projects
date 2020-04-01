# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:46:22 2020

@author: Yongyao SUN
"""

'''
2. 简单shopify 监控器

- 支持如undefeated网站的单品尺码监控，即当监控的单品更新尺码时，发送提醒到自定义的webhook
- 支持自定义webhook
- 做好错误处理，需要能够长期运行
- 附加题 实现undfeated的上新监控

hint:
- 对于一个单品 如 https://undefeated.com/collections/all/products/nike-x-undefeated-air-max-90-pacificblue-vividpurple 可以在后面加.json获取一个json的页面(shopify特性)
- https://undefeated.com/products.json 可以看到一个shopify站的所有商品（某些站会关闭，但本project只要实现未关闭的站即可)
'''

from discord import Webhook, RequestsWebhookAdapter, Embed
import your_info
import requests
import datetime
import random
import json
import time


def loadProxyUserPass(filename):
    proxyList = []
    with open(filename + '.txt') as f:
        file_content = f.read()
    file_rows = file_content.split('\n')
    for i in range(0, len(file_rows)):
        if ':' in file_rows[i]:
            tmp = file_rows[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)
    return proxyList 

def loadProxyIpAuth(filename):
    proxyList = []
    with open(filename + '.txt') as f:
        file_content = f.read()
    tmp = file_content.split('\n')
    for n in range(0, len(tmp)):
        if ':' in tmp[n]:
            temp = tmp[n]
            proxies = {'http': 'http://' + temp,  'https': 'http://' + temp}
            proxyList.append(proxies)
    return proxyList

class shopify_monitor:
    def __init__(self, author, avatar, webhook, url, website):
        self.author = author
        self.avatar = avatar
        self.webhook = webhook
        self.url = url
        self.website = website
        
    def webhook_single(self,image_url,atc_url,price,size_available,name,url):
        webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
        embed = Embed(title=self.website,description="[{}]({})".format(name,url),colour=65280)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=self.author, icon_url=self.avatar)\
            .set_thumbnail(url=image_url)\
            .add_field(name="Price", value=price)
        atc = []
        for i in range(len(size_available)):
            atc.append("[{}]({})".format(size_available[i],atc_url[i]))
        atc = str(atc).lstrip('[')\
            .rstrip(']')\
            .replace('\'','')\
            .replace(',','\n')
        embed.add_field(name="Size",value=atc,inline=True)
        webhook.send(embed=embed)
    
    def webhook_new_product(self,product_name):
        url_product = self.website+'/products/'+product_name
        url = url_product+'.json'
        headers = {
        			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        		}
        size_available = []
        try:
            r = requests.get(url,headers=headers)
            product = json.loads(r.text)['product']
            for variant in product['variants']:
                if variant['inventory_quantity']>0:
                    size_available.append(variant['title'])
            image_url,atc_url,price,name=self.parse_single(product)
            if atc_url:
                self.webhook_single(image_url,atc_url,price,size_available,name,url_product)
        except Exception as e:
            print("失败，exception {} response {}".format(e,r.status_code))
    
    def parse_single(self,product):
        image_url = product['image']['src']
        price = str(product['variants'][0]['price'])
        name = product['handle']
        atc_url = []
        for variant in product['variants']:
            if variant['inventory_quantity']>0:
                atc_url.append('{}/cart/{}:1'.format(self.website,variant['id']))
        return image_url,atc_url,price,name
        
    def singele_product(self,url):
        try:
            proxyList = loadProxyUserPass('proxies')
        except:
            proxyList = loadProxyIpAuth('proxies')
        url = url+'.json'
        headers = {
        			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        		}
        size_available = []
        old_size_available = []
        while True:
            try:
                if proxyList:
                    r = requests.get(url,headers=headers,proxies=random.choice(proxyList))
                else:
                    r = requests.get(url,headers=headers)
                product = json.loads(r.text)['product']
                for variant in product['variants']:
                    if variant['inventory_quantity']>0:
                        size_available.append(variant['title'])
                if old_size_available == size_available:
                    print('Stock dosen\'t change...')
                    time.sleep(5)
                    continue
                else:
                    print('Stock change!!!')
                    image_url,atc_url,price,name=self.parse_single(product)
                    self.webhook_single(image_url,atc_url,price,size_available,name,self.url)
                    old_size_available = size_available
            except Exception as e:
                print("失败，exception {} response {}".format(e,r.status_code))
            time.sleep(5)
            
    def new_product(self,website):
        try:
            proxyList = loadProxyUserPass('proxies')
        except:
            proxyList = loadProxyIpAuth('proxies')
        headers = {
    			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    		}
        website_url = website+'/products.json'
        prodduct_available = []
        old_prodduct_available = []
        while True:
            try:
                if proxyList:
                    r = requests.get(website_url,headers=headers,proxies=random.choice(proxyList))
                else:
                    r = requests.get(website_url,headers=headers)
                products = json.loads(r.text)
                for product in products['products']:
                    prodduct_available.append(product['handle'])
                if old_prodduct_available == prodduct_available:
                    print('No new products')
                    time.sleep(5)
                    continue
                else:
                    print('Found new producrs!!!')
                    for i in range(len(prodduct_available)):
                        if prodduct_available[i] in old_prodduct_available:
                            prodduct_available.remove(prodduct_available[i])
                        else:
                            self.webhook_new_product(prodduct_available[i])
                            time.sleep(3)
                    old_prodduct_available = prodduct_available
            except Exception as e:
                print("失败，exception {} response {}".format(e,r.status_code))
            time.sleep(10)
        
def main():
    author = your_info.your_discord_name()
    avatar = your_info.your_discord_avatar()
    webhook = your_info.homework_webhook()
    website = 'https://www.dope-factory.com'
    url = 'https://www.dope-factory.com/products/nike-air-force-1-type-cq2344-101'
    monitor = shopify_monitor(author, avatar, webhook, url, website)
    monitor.singele_product(url)
    monitor.new_product(website)
    
main()
