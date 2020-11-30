from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
import time
import json
import discord

class AnchorBot:

    def __init__(self):
        # Build up auth for browser 
        options = Options()
        options.headless = True
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(options=options)        
        
    def login(self):
        # Login to anchor.fm
        bot = self.bot
        bot.get('https://anchor.fm/login')
        time.sleep(9)
        
        email = bot.find_element_by_name('email')
        password = bot.find_element_by_name('password')
        
        email.clear()
        password.clear()
        
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        
    def exec(self):
        token = os.environ['TOKEN']
        client = discord.Client()

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
                
            if message.content == 'stats!':
                anchorbot.login()
                time.sleep(9)
                bot = self.bot
                friendly = 'Here are the current Beers in The Lot Podcast stats from anchor.fm.'
                stats = set()
                stats = map(lambda el: el.text, bot.find_elements_by_xpath("//div[@class = 'css-uzrgbc']"))
                await message.channel.send(friendly)
                for stat in stats:
                    await message.channel.send(stat)

        client.run(token)

anchorbot = AnchorBot()

anchorbot.exec()