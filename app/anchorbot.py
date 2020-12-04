from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from PIL import Image
import io
import os
import time
import discord
from discord.ext import commands

class AnchorBot:

    def __init__(self):
        # Build up auth for browser 
        options = Options()
        options.headless = True
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox(options=options)
        snapshot_image_path = 'snapshot_screenshot.png'        
        weekly_image_path = 'weekly_screenshot.png'
        self.snapshot_image_path = snapshot_image_path
        self.weekly_image_path = weekly_image_path

    def login(self):
        # Login to anchor.fm
        browser = self.browser
        browser.get('https://anchor.fm/login')
        time.sleep(5)
        email = browser.find_element_by_name('email')
        password = browser.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def genimg(self):
        # Generate screenshots
        anchorbot.login()
        time.sleep(12)
        browser = self.browser
        # Generates boxscore stats screenshot
        snapshot_image = browser.find_element_by_xpath("//div[@class = 'css-av84af']").screenshot_as_png
        snapshot_imageStream = io.BytesIO(snapshot_image)
        snapshot_im = Image.open(snapshot_imageStream)
        snapshot_im.save(self.snapshot_image_path)
        # Generates weekly total plays screenshot
        weekly_image = browser.find_element_by_xpath("//div[@class = 'VictoryContainer']").screenshot_as_png
        weekly_imageStream = io.BytesIO(weekly_image)
        weekly_im = Image.open(weekly_imageStream)
        weekly_im.save(self.weekly_image_path)
        
    def exec(self):
        # The Discord bot
        token = os.environ['TOKEN']
        role = os.environ['ROLE']
        bot = commands.Bot(command_prefix='!')
        @bot.command(name='stats')
        @commands.has_role(role)
        async def anchor_stats(ctx):
            anchorbot.genimg()
            snapshot_stats = 'Here are the current Beers in The Lot Podcast stats from anchor.fm.'
            weekly_stats = 'Here is the total plays per week trend.'
            await ctx.send(snapshot_stats)
            await ctx.channel.send(file=discord.File(self.snapshot_image_path))
            await ctx.channel.send(weekly_stats)
            await ctx.channel.send(file=discord.File(self.weekly_image_path))
        bot.run(token)

anchorbot = AnchorBot()

anchorbot.exec()