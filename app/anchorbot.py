from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from PIL import Image
import io
import os
import time
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
        time.sleep(5)
        
        email = bot.find_element_by_name('email')
        password = bot.find_element_by_name('password')
        
        email.clear()
        password.clear()
        
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def genimg(self):
        anchorbot.login()
        time.sleep(12)
        bot = self.bot

        snapshot_image_path = 'snapshot_screenshot.png'
        snapshot_image = bot.find_element_by_xpath("//div[@class = 'css-av84af']").screenshot_as_png
        snapshot_imageStream = io.BytesIO(snapshot_image)
        snapshot_im = Image.open(snapshot_imageStream)
        snapshot_im.save(snapshot_image_path)

        weekly_image_path = 'weekly_screenshot.png'
        weekly_image = bot.find_element_by_xpath("//div[@class = 'VictoryContainer']").screenshot_as_png
        weekly_imageStream = io.BytesIO(weekly_image)
        weekly_im = Image.open(weekly_imageStream)
        weekly_im.save(weekly_image_path)
        
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
                anchorbot.genimg()
                time.sleep(6)
                bot = self.bot
                snapshot_image_path = 'snapshot_screenshot.png'
                weekly_image_path = 'weekly_screenshot.png'
                snapshot_stats = 'Here are the current Beers in The Lot Podcast stats from anchor.fm.'
                weekly_stats = 'Here is the total plays per week trend.'
                await message.channel.send(snapshot_stats)
                await message.channel.send(file=discord.File(snapshot_image_path))
                await message.channel.send(weekly_stats)
                await message.channel.send(file=discord.File(weekly_image_path))

        client.run(token)

anchorbot = AnchorBot()

anchorbot.exec()