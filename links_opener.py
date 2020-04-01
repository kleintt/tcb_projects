# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 13:44:58 2020

@author: Yongyao SUN
"""

import pandas as pd
import cloudscraper
import progressbar

def loadProxyUserPass(proxy):
    proxyList = []
    for i in range(0, len(proxy)):
        if ':' in proxy[i]:
            tmp = proxy[i]
            tmp = tmp.split(':')
            proxies = {'http': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/',
                       'https': 'http://' + tmp[2] + ':' + tmp[3] + '@' + tmp[0] + ':' + tmp[1] + '/'}
            proxyList.append(proxies)
    return proxyList 


def loadProxyIpAuth(proxy):
    proxyList = []
    for n in range(0, len(proxy)):
        if ':' in proxy[n]:
            temp = proxy[n]
            proxies = {'http': 'http://' + temp,  'https': 'http://' + temp}
            proxyList.append(proxies)
    return proxyList 

def links_import():
    data = pd.read_csv('links.csv')
    links = list(data['link'].values)
    proxy = list(data['proxy'].values)
    return data,links,proxy

def status_write(i,status,data):
    data['status'][i] = status
    data.to_csv('links.csv',index=False)

def main():
    print('Loading links and proxy...')
    data,links,proxy = links_import()
    print('Load {} links and {} proxies'.format(len(links),len(proxy)))
    try:
        proxyList = loadProxyUserPass(proxy)
    except:
        proxyList = loadProxyIpAuth(proxy)
    print('Starting open links...')
    p = progressbar.ProgressBar()
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            }
    with open( '2captcha.txt') as f:
        api_key = f.read()
    for i in p(range(len(links))):
        scraper = cloudscraper.create_scraper(interpreter='nodejs',
                                          recaptcha={
                                            'provider': '2captcha',
                                            'api_key': api_key
                                          })
        try:
            r = scraper.get(links[i],headers=headers,proxies=proxyList[i])
            if r.status_code == 200 or r.status_code == 301:
                print('Successful')
                status = 'Successful'
                status_write(i,status,data)
            else:
                print('Retrying')
                scraper = cloudscraper.create_scraper(interpreter='nodejs',
                                          recaptcha={
                                            'provider': '2captcha',
                                            'api_key': api_key
                                          })
                r = scraper.get(links[i],headers=headers,proxies=proxyList[i])
                if r.status_code == 200 or r.status_code == 301:
                    print('Successful')
                    status = 'Successful'
                    status_write(i,status,data)
                else:
                    print('Failed')
                    status = 'Failed'
                    status_write(i,status,data)
        except:
            print('Failed')
            status = 'Failed'
            status_write(i,status,data)

if __name__ == "__main__":
    main()
    