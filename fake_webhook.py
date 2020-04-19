# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:48:34 2020

@author: Yongyao SUN
"""

'''

1. fake webhook 模拟器

- 支持 Cyber, Tks, Balko 等主流bot的 webhook 格式(在程序中可以自主选择最好，可以使用input()来实现)
- 支持自己输入webhook信息，如单品标题，尺码，profile名称，标题图片等信息
- 支持自定义webhook link
- 支持自定义 webhook发送的author名字以及author avatar(头像)

'''

from discord import Webhook, RequestsWebhookAdapter, Embed
import your_info
import datetime
import json
from pick import pick

class fake_webhook:
    def __init__(self, author, avatar, webhook, bot, info):
        self.author = author
        self.avatar = avatar
        self.webhook = webhook
        self.bot = bot
        self.info = info

    def cyber(self):
        webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
        embed = Embed(title='Successfully checked out!',description=self.info['cyber']['Product'],colour=65280)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=self.author, icon_url=self.avatar)\
            .set_thumbnail(url=self.info['cyber']['url'])\
            .add_field(name="Store", value=self.info['cyber']['Store'])\
            .add_field(name="Size", value=self.info['cyber']['Size'])\
            .add_field(name="Profile", value="||"+self.info['cyber']['Profile']+"||")\
            .add_field(name="Order", value="||"+self.info['cyber']['Order']+"||")\
            .add_field(name="Proxy List", value="||"+self.info['cyber']['ProxyList']+"||")\
            .add_field(name="Color", value=self.info['cyber']['Color'])\
            .add_field(name="Category", value=self.info['cyber']['Category'])\
            .add_field(name="3D Secure", value=self.info['cyber']['3D'])\
            .add_field(name="Mode", value=self.info['cyber']['Mode'])\
            .set_footer(text="CyberAIO",icon_url="https://images-ext-2.discordapp.net/external/AFl8btw6-OdaFIC4DU6c8as5gTG8SIVdsOx_hLOXnEs/https/cdn.cybersole.io/media/discord-logo.png?width=672&height=672")
        webhook.send(embed=embed)
    
    def tks(self):
        content = 'Success:'+self.info['tks']['Product']
        webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
        embed = Embed(title='You cooked',colour=10053324)
        embed.set_author(name=self.author, icon_url=self.avatar)\
            .set_thumbnail(url=self.info['tks']['url'])\
            .add_field(name="Website", value=self.info['tks']['Website'])\
            .add_field(name="Product", value=self.info['tks']['Product'])\
            .add_field(name="Size", value="||"+self.info['tks']['Size']+"||")\
            .add_field(name="Price", value=self.info['tks']['Price'])\
            .add_field(name="Link", value=self.info['tks']['url'])\
            .add_field(name="Profile", value="||"+self.info['tks']['Profile']+"||")\
            .add_field(name="Proxy", value="||"+self.info['tks']['Proxy']+"||")\
            .add_field(name="Time stamp(utc)", value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%p'))\
            .add_field(name="Order id", value="||"+self.info['tks']['OrderId']+"||")\
            .add_field(name='Checkout delay',value=self.info['tks']['CheckoutDelay'])
        webhook.send(content,embed=embed)
    
    def bnb(self):
        webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
        embed = Embed(title='Succesfully checked out a product.')
        embed.set_author(name=self.author, icon_url=self.avatar)\
            .set_thumbnail(url=self.info['bnb']['url'])\
            .add_field(name="Product", value=self.info['bnb']['Product'])\
            .add_field(name="Style Code", value=self.info['bnb']['StyleCode'])\
            .add_field(name="Size", value=self.info['bnb']['Size'])\
            .add_field(name="Email", value=self.info['bnb']['Email'])\
            .set_footer(text="via Better Nike Bot",icon_url="https://cdn.discordapp.com/icons/522807268811472937/9adeacd23141d2dfce086ea2a225ce98.png?size=128")
        webhook.send(embed=embed)
    
def main():
    author = your_info.your_discord_name()
    avatar = your_info.your_discord_avatar()
    webhook = your_info.homework_webhook()
    with open("webhook_info.json",'r',encoding='utf-8') as load_json:
        info = json.load(load_json)
    options = ["cyber", "tks", "bnb"]
    title = "Please select a bot: "
    bot, index = pick(options, title)
    webhook_bot = fake_webhook(author,avatar,webhook,bot,info)
    if bot == 'cyber':
        webhook_bot.cyber()
    elif bot == 'tks':
        webhook_bot.tks()
    else:
        webhook_bot.bnb()
main()