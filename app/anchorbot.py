from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
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
        executable = GeckoDriverManager().install()
        options = Options()
        options.headless = True
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox(executable_path=executable, options=options)
        snapshot_image_path = 'snapshot_screenshot.png'        
        weekly_image_path = 'weekly_screenshot.png'
        charts_image_path = 'charts_screenshot.png'
        self.snapshot_image_path = snapshot_image_path
        self.weekly_image_path = weekly_image_path
        self.charts_image_path = charts_image_path

    def anchor_login(self):
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

    def anchor_genimg(self):
        # Generate screenshots
        anchorbot.anchor_login()
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

    def chartable_genimg(self):
        # Open Chartable
        chartable_url = os.environ['CHARTABLE']
        browser = self.browser
        browser.get(chartable_url)
        time.sleep(8)
        popup = browser.find_elements_by_xpath("//a[@class = 'link pa2 bg-blue white br2']")
        if popup:
            popup[0].click()
            time.sleep(1)
        else:
            time.sleep(1)
        # Generates Charts screenshot
        charts = browser.find_elements_by_xpath("//table[@class = 'w-100 f5 mb1']")
        if charts:
            charts_image = charts[0].screenshot_as_png
            charts_imageStream = io.BytesIO(charts_image)
            charts_im = Image.open(charts_imageStream)
            charts_im.save(self.charts_image_path)
            time.sleep(1)
        else:
            time.sleep(1)

    def exec(self):
        # The Discord bot
        token = os.environ['TOKEN']
        role = os.environ['ROLE']
        bot = commands.Bot(command_prefix=':bitl_stats:')
        @bot.command(name='get')
        @commands.has_role(role)
        async def anchor_stats(ctx):
            anchorbot.anchor_genimg()
            anchorbot.chartable_genimg()
            snapshot_stats = 'Here are the current podcast stats from anchor.fm.'
            no_snapshot_stats = 'Podcast stats from anchor.fm are unavailable right now.'
            weekly_stats = 'Here is the total plays per week trend.'
            no_weekly_stats = 'The total plays per week stats are unavailable right now.'
            charts_stats = 'Here is where the podcast ranks on Apple Podcasts Charts'
            no_charts_stats = 'The Apple Podcast Charts are currently not available.'
            if os.path.isfile(self.snapshot_image_path):
                await ctx.send(snapshot_stats)
                await ctx.channel.send(file=discord.File(self.snapshot_image_path))
            else:
                await ctx.send(no_snapshot_stats)
            if os.path.isfile(self.weekly_image_path):
                await ctx.channel.send(weekly_stats)
                await ctx.channel.send(file=discord.File(self.weekly_image_path))
            else:
                await ctx.channel.send(no_weekly_stats)
            if os.path.isfile(self.charts_image_path):
                await ctx.channel.send(charts_stats)
                await ctx.channel.send(file=discord.File(self.charts_image_path))
            else:
                await ctx.channel.send(no_charts_stats)
        bot.run(token)

anchorbot = AnchorBot()

anchorbot.exec()