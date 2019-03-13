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
    - win sneaking ('pihistys') if you can win with last reel, slowroll it

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
'''
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
'''
payTable = {
    'AAA': 10000,
    'BBB': 1000,
    'CCC': 500,
    'DDD': 250,
    'DDX': 50,
    'EEE': 200,
    'EEX': 10,
    'FFF': 20,
    'XFF': 4,
    'XXF': 1.4,
    'GGG': 5,
    'GGX': 3,
    'GXX': 1.2,
    'HHH': 1.5
}

symbolTable = {
    'A': '⭐',
    'B': '🍑',
    'C': '🍊',
    'D': '🍓',
    'E': '🍒',
    'F': '🍋',
    'G': '🍉',
    'H': '🍍'

}

def populateReel(reelNo, symbolsReel):
    currentSymbol = ''
    currentSymbolNo = 0

    for x in symbolsReel:
        currentSymbol = symbolOrder[currentSymbolNo]
        
        for i in range(x):
                reelNo.append(currentSymbol)
        
        currentSymbolNo += 1
    print('reel populated!')

# symbolOrder = ['⭐', '🍑', '🍊', '🍓', '🍒', '🍋', '🍉', '🍍']  
symbolOrder = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  
reelOneSymbols   = [1, 5, 6, 5, 8, 18, 11, 31]
reelTwoSymbols   = [1, 7, 4, 5, 8, 13, 14, 33]
reelThreeSymbols = [1, 2, 6, 11, 5, 9, 18, 33]

reelOne = []
populateReel(reelOne, reelOneSymbols)

reelTwo = []
populateReel(reelTwo, reelTwoSymbols)

reelThree = []
populateReel(reelThree, reelThreeSymbols)



@juicyBot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(juicyBot))

@juicyBot.command()
async def test(fruit):
    await fruit.send('Melon: 🍉')


@juicyBot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@juicyBot.command()
async def spin(slots, betAmount: int):
    minAmount = 0.2
    maxAmount = 50
    lineWin = ''
    isWin = False
    winAmount = 0
    author = slots.message.author.name

    if (betAmount > minAmount and betAmount < maxAmount):
        reelsMsg = await slots.send('.\n:gem: Spinning reels :gem:')
        await reelsMsg.add_reaction("\U0001F611") # 😑
        reel1 = random.choice(reelOne)
        reel1Symbol = symbolTable[reel1]
        await reelsMsg.add_reaction("\U0001F610") # 😐
        reel2 = random.choice(reelTwo)
        reel2Symbol = symbolTable[reel2]
        await reelsMsg.add_reaction("\U0001F62E") # 😮
        reel3 = random.choice(reelThree)
        reel3Symbol = symbolTable[reel3]
        # 
        await reelsMsg.clear_reactions()
        await reelsMsg.edit(content=reelsMsg.content + '\n:gem: |' + reel1Symbol)
        await reelsMsg.edit(content=reelsMsg.content + '|' + reel2Symbol)
        await reelsMsg.edit(content=reelsMsg.content + '|' + reel3Symbol + '| :gem:')
        #
        lineWin = reel1 + reel2 + reel3
        print(lineWin)
    else:
        # insufficient funds
        # too small/large bet
        # other ?
        await slots.send('...error...')
        return
    
    for win in payTable:
        if (win == lineWin):
            winAmount = betAmount * payTable[win]
            isWin = True
    
    if (isWin):
        await slots.send('{0} played {1} jC and won {2}'.format(author, betAmount, winAmount))
    else:
        await slots.send('{} loses :('.format(author))


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
