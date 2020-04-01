# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:43:34 2020

@author: Yongyao SUN
"""

'''
5. 简单的proxy筛选脚本

- 通过对google的request测试来测试proxy连通性（ 如果你想支持别的网站，可以作为附加项）
- 利用requests 模块实现
- 每条proxy，最好测试多次取其平均值，因为网络有其不稳定性
- 输入为一个proxy列表的txt
- 输出为一个筛选过可以达到程序设置要求的proxy列表（延迟小于 xxx ms)
- 要求在console输出每条proxy的延迟结果

hint:
- requests 的 proxy使用，需要https和http proxy都设置才会生效，并且格式不一样
- 运行该脚本不要再你的本地运行, 需要去服务器或者国外的local
- 延迟设定要根据你的网络情况来决定
'''

import time
import requests
import numpy as np

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

def main():
    threshold = int(input('请输入延迟上限:\n'))
    try:
        proxyList = loadProxyUserPass('proxies')
    except:
        proxyList = loadProxyIpAuth('proxies')
    with open('proxies.txt') as f:
        proxy_List = f.read()
    proxy_List = proxy_List.split('\n')
    print(f'Loaded {len(proxyList)} proxies')
    for i in range(len(proxyList)):
        speed = []
        for j in range(5):
            try:
                r = requests.get('https://www.google.com/',timeout=5,proxies=proxyList[i])
                speed.append(r.elapsed.microseconds/1000)
            except Exception as e:
                    print("失败，exception {} response {}".format(e,r.status_code))
            time.sleep(1)
        if np.mean(speed) <= threshold:
            print(f'{proxy_List[i]}  speed: {np.mean(speed)}')
            file = open('fast_proxies.txt', 'a')
            file.write(str(proxy_List[i].replace('\'', '')))
            file.write("\n")
            file.close()
        else:
            print(f'{proxy_List[i]}  speed: {np.mean(speed)}')
main()