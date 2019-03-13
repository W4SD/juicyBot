# juicyBot2.py
# Python 3.7.0
# discord.py-rw (1.0)
# DEVELOPMENT VERSION

import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random

'''
Discord bot for general help and gambling related activity
@toDo: (general)
    - prefix used, command not found response
    - announce if streamer is online
@toDo: (features)
    - coinFlip
    - dicing
    - mySql support
    - user based wallet
    - "juicyTokens" -economy system
    - other gambling games
@toDo: (juicySlots)
    - asyncio delay for winning emojis

'''

'''
3-reel juicySlots
Unicodes: U000 +
⭐ = :star: / 2B50
🍑 = :peach: / 1F351
🍊 = :tangerine: / 1F34A
🍓 = :strawberry: / 1F353
🍒 = :cherries: / 1F352
🍋 = :lemon: / 1F34B
🍉 = :watermelon: / 1F349
🍍 = :pineapple: / 1F34D

'''

# define globals
PREFIX = '€'

juicyBot = commands.Bot(command_prefix=PREFIX, description="bot in development!")

# YouTube link auto titler


def isYoutubeLink(message):
    if message.content.startswith('https://www.youtube.com/') or message.content.startswith('https://youtu.be/'):
        return True
    else:
        return False

def tubeTitler(message):
    try:
        url = message.content
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        splitTitle = soup.title.string.split(' - YouTube')  # remove ' - Youtube' string from title
        r_message = 'Video: ' + str(splitTitle[0])
        return r_message

    except Exception as e:
        print('err_tubeLink: ' + message.content)
        print(e)

# juicyReels

print('Creating reels')

payTable = {
    '⭐⭐⭐': 10000,
    '🍑🍑🍑': 1000,
    '🍊🍊🍊': 500,
    '🍓🍓🍓': 250,
    '🍓🍓x': 50,
    '🍒🍒🍒': 200,
    '🍒🍒x': 10,
    '🍋🍋🍋': 20,
    'x🍋🍋': 4,
    'xx🍋': 1.4,
    '🍉🍉🍉': 5,
    '🍉🍉x': 3,
    '🍉xx': 1.2,
    '🍍🍍🍍': 1.5
}

@juicyBot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(juicyBot))


@juicyBot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@juicyBot.command()
async def spin(slots, betAmount: int):
    minAmount = 0.2
    maxAmount = 50

    author = slots.message.author.name

    if (betAmount > minAmount and betAmount < maxAmount):
        reelsMsg = await slots.send('.\n:gem: Spinning reels :gem:')
        await reelsMsg.add_reaction("\U0001F611") # 😑
        await reelsMsg.add_reaction("\U0001F610") # 😐
        await reelsMsg.add_reaction("\U0001F62E") # 😮
        # 
        await reelsMsg.clear_reactions()
        await reelsMsg.edit(content=reelsMsg.content + '\n:gem: |:watermelon:')
        await reelsMsg.edit(content=reelsMsg.content + '|:watermelon:')
        await reelsMsg.edit(content=reelsMsg.content + '|:watermelon:| :gem:')
    else:
        # insufficient funds
        # too small/large bet
        # other ?
        await slots.send("...error...")
        return
    await slots.send("{0} played {1} jC and won?".format(author, betAmount))


@juicyBot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == juicyBot.user:
        pass
    else:
        try:
            print(str(message.content))
            if (isYoutubeLink(message)):
                await message.channel.send(tubeTitler(message))
            else:
                await juicyBot.process_commands(message)
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print('@juicyBot.event' + str(e))


try:
    # paste bot secret token to plain .txt file
    tokenFile = open("discoToken.txt", "r")
    token = tokenFile.readline()
    tokenFile.close()
except Exception as e:
    print(e)

juicyBot.run(token)
