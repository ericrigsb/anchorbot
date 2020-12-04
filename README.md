# AnchorBot

Python based Discord bot that logs into an Anchor.fm podcast account, takes screenshots of some of the stats in the dashboard, and sends those screenshots to a Discord server.

Requires a Docker container that has Firefox and the geckodriver installed.

Requires an existing Discord application and bot be established in the Discord developer portal.

The bot established in the developer portal will require send message privileges when establishing the bot OAuth. In the channel you want the bot to respond to commands in, the bot will need read message privileges.

Reference to get started: https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal

## Install and Run the Bot

`git clone https://github.com/ericrigsb/anchorbot.git`

`cd anchorbot`

Adjust the image parameter in docker-compose.yml as necessary.

Copy .env.sample to .env and enter values for Anchor.fm username and password; and Discord bot token (see above regarding application and bot requirement) and Discord server role you want to allow to invoke the bot.

Run `docker-compose up`

## Invoking the bot on Discord

Simply enter `!stats` and wait some time while the bot grabs the screenshots.