# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:10:46 2020

@author: Yongyao SUN
"""

'''
4. 可以自动gen resi proxy 并且分给不同bot的proxy脚本

- 以smart为例，如果你用过oxy geo 或者netnut，请自行扩展，不要求支持多家proxy，但能支持是附加分
- 自行获取smart的地区列表
- 输入为 你想要的地区（可能是一个地区列表），你想要使用的bot(一个bot列表), 以及每个bot想要多少条proxy
- 输出直接是当前目录下的文件，为 bot名字开头的txt文件，分别代表给每个bot生成的 proxy 列表

hint:
- smart的地区列表请自行到smart官网注册账号查看(或者到resi game 的dc server中查看)
- 请自行研究smart proxy的resi generate规则并写成程序
- 请使用 random 这个模块
'''

import random
import string
import json
import pandas as pd

def get_country():
    # Smart
    smart = pd.read_csv('smart.csv')
    smart = list(smart.iloc[:,0].values)
    smart_country = []
    for i in range(len(smart)):
        tmp = smart[i].split('.')
        smart_country.append(tmp[0])
    smart_country = list(set(smart_country))
    smart_country.remove('gate')
    smart_country.remove('city')
    
    # Smart port
    smart_port = {}
    old = 'gate'
    for i in range(len(smart)):
        new = smart[i].split('.')[0]
        port = smart[i].split(':')[1]
        if i == 0:
            smart_port[f'{new}'] = [port]
            old = new
        if old != new and i >=1:
            smart_port[f'{new}'] = [port]
            smart_port[f'{old}'].append(smart[i-1].split(':')[1])  
            old = new
    smart_port.pop('gate')
    smart_port.pop('city')
    with open("smart_port.json","w") as f:
        json.dump(smart_port,f)
    
    # Oxylab
    oxylab = pd.read_csv('oxylab.csv')
    oxylab = list(oxylab['Country'].values)
    oxylab_country = list(set(oxylab))
    oxylab_country.pop(0)
    
    # Geosurf
    geosruf = pd.read_csv('geosurf.csv')
    geosruf = list(geosruf['ctr'].values)
    geosruf_country = list(set(geosruf))
    geosruf_country.pop(0)
    
    country_dict = {
            'smart':smart_country,
            'oxylab':oxylab_country,
            'geosurf':geosruf_country
            }
    with open("country_dict.json","w") as f:
        json.dump(country_dict,f)

def smart_gen(amount,country,user,pw):
    with open("country_dict.json",'r') as country_dict:
        country_dict = json.load(country_dict)
    smart_country = country_dict['smart']
    with open("smart_port.json",'r') as smart_port:
        smart_port = json.load(smart_port)
    amount = int(amount)
    proxy_list = []
    if type(country) == str:
        if country in smart_country:
            port_begin = int(smart_port[country][0])
            port_end = int(smart_port[country][1])
            num_port = port_end-port_begin+1
            if amount > num_port:
                amount = num_port
            for i in range(amount):
                proxy_list.append(f'{country}.smartproxy.com:{i+port_begin}:{user}:{pw}')
        else:
            print(f'Invalid country: {country}')

    for j in range(len(country)):
        
        if country[j].lower() in smart_country:
            port_begin = int(smart_port[country[j]][0])
            port_end = int(smart_port[country[j]][1])
            num_port = port_end-port_begin+1
            if amount > num_port:
                amount = num_port
            for l in range(amount):
                proxy_list.append(f'{country[j]}.smartproxy.com:{l+port_begin}:{user}:{pw}')
        else:
            print(f'Invalid country: {country[j]}')
            continue
    return proxy_list

def oxylab_gen(amount,country,user,pw):
    with open("country_dict.json",'r') as country_dict:
        country_dict = json.load(country_dict)
    oxylab_country = country_dict['oxylab']
    proxy_list = []
    if type(country) == str:
        if country.upper() in oxylab_country:
            for i in range(int(amount)):
                session = random.random()
                proxy_list.append(f'pr.oxylabs.io:7777:customer-{user}-cc-{country}-sessid-{session}-sesstime-60:{pw}')
        else:
            print(f'Invalid country: {country}')

    for j in range(len(country)):
        if country[j].upper() in oxylab_country:
            for l in range(amount):
                session = random.random()
                proxy_list.append(f'pr.oxylabs.io:7777:customer-{user}-cc-{country[j]}-sessid-{session}-sesstime-60:{pw}')
        else:
            print(f'Invalid country: {country[j]}')
            continue
    proxy_list = list(set(proxy_list))
    return proxy_list


def geosurf_gen(amount,country,user,pw):
    with open("country_dict.json",'r') as country_dict:
        country_dict = json.load(country_dict)
    geosurf_country = country_dict['geosurf']
    proxy_list = []
    if type(country) == str:
        if country.upper() in geosurf_country:
            for i in range(int(amount)):
                ran_num = ''.join(random.sample(string.digits, 6))
                proxy_list.append(f'{country}-30m.geosurf.io:8000:{user}+{country}+{user}-{ran_num}:{pw}')
        else:
            print(f'Invalid country: {country}')

    for j in range(len(country)):
        if country[j].upper() in geosurf_country:
            for l in range(int(amount)):
                ran_num = ''.join(random.sample(string.digits, 6))
                proxy_list.append(f'{country[j]}-30m.geosurf.io:8000:{user}+{country[j]}+{user}-{ran_num}:{pw}')
        else:
            print(f'Invalid country: {country[j]}')
            continue
    proxy_list = list(set(proxy_list))
    return proxy_list

def main():
    country = input('请输入需要生成的国家(多个国家请用英文;分开)\n')
    bot = input('请输入使用的Bot(多个Bot请用英文;分开)\n')
    amount = input('请输入每个Bot需要proxy的数量(请按照顺序，多个请用英文;分开)\n')
    provider = input('请输入需要哪家provider(smart,oxylab,geosurf):\n')
    user = input('请输入用户名\n')
    pw = input('请输入密码\n')
    country_list = country.split(';')
    bot_list = bot.split(';')
    amount_list = amount.split(';')
    for i in range(len(bot_list)):
        if provider == 'smart':
            proxy_list = smart_gen(amount_list[i],country_list,user,pw)
        elif provider == 'oxylab':
            proxy_list = oxylab_gen(amount_list[i],country_list,user,pw)
        elif provider == 'smart':
            proxy_list = geosurf_gen(amount_list[i],country_list,user,pw)
        else:
            print('大兄弟，输错provider的名字了')
        print(f"生成{bot_list[i]}的proxies中")
        file = open(f'{bot_list[i]}.txt', 'w')
        for i in range(len(proxy_list)):
            file.write(str(proxy_list[i].replace('\'', '')))
            file.write("\n")
        file.close()
        print("生成完毕！")
main()
        
    
    
    
