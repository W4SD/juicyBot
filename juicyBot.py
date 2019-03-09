# juicyBot.py
# Python 3.6.7
# DEVELOPMENT VERSION

import discord
import requests
import json
import random
from bs4 import BeautifulSoup

'''
Discord bot for general help and gambling related activity
@toDo: (general)
    - prefix used, command not found response
@toDo: (features)
    - coinFlip
    - dicing
    - mySql support
    - user based wallet
    - "juicyTokens" -economy system
    - other gambling games

'''

# define globals
PREFIX = '€'


# command handler class


class CommandHandler:

    # constructor
    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(PREFIX + command['trigger']):
                args = message.content.split(' ')
                if args[0] == PREFIX + command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                            break
                        else:
                            return self.client.send_message(message.channel,
                                                            'command "{}" requires {} argument(s) "{}"'.format(command['trigger'],
                                                             command['args_num'],
                                                             ', '.join(command['args_name'])))
                            break
                else:
                    break

            else:
                if message.content.startswith('https://www.youtube.com/') or message.content.startswith('https://youtu.be/'):
                    return self.client.send_message(message.channel, 'Video: "{}"'.format(tubeTitler(message.content)))
                    break


# create discord client
client = discord.Client()
try:
    tokenFile = open("discoToken.txt", "r") # paste bot secret token to plain .txt file
    token = tokenFile.readline()
    tokenFile.close()
except Exception as e:
    print(e)

# create the CommandHandler object and pass it the client
ch = CommandHandler(client)

# start commands command


def commands_command(message, client, args):
    try:
        count = 1
        coms = 'Command list:\n'
        for command in ch.commands:
            coms += '{}{} : {}\n'.format(PREFIX,
                                         command['trigger'],
                                         command['description'])
            count += 1
        return coms
    except Exception as e:
        print('err@commands_command' + str(e))


ch.add_command({
    'trigger': 'help',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'All my command are belong to us!'
})
# end commands command

# general info command


def postInfo(message, client, args):
    textLines = []
    textLines.append('paste a youtube link and I will automagically post the title!')

    infoText = ':)\nWhat else I can do for you:\n'
    for i in textLines:
        infoText += '- {}\n'.format(i)

    return infoText

ch.add_command({
    'trigger': 'info',
    'function': postInfo,
    'args_num': 0,
    'args_name': [],
    'description': 'How can I help you today?'
})



# coin flip

'''
def coinFlip(message, client, args):
    try:

    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!flip',
    'function': coinFlip,
    'args_num': 1,
    'args_name': [],
    'description': 'Flips a coin and prints result'
})
'''

# 3-reel emo slots

# class Reel():

def test():
    @client.event


def spinSlots(message, client, args):
    try:
        await client.send_message(message.channel, 'MORO')
        winMessage = 'U lose sry! ;)'

        return winMessage

    except Exception as e:
        print(e)

ch.add_command({
    'trigger': 'spin',
    'function': spinSlots,
    'args_num': 1,
    'args_name': ['Bet amount 0.20-50'],
    'description': 'Spin some reels! :slot_machine:'
})

# youtube link titler


def tubeTitler(tubeLink):
    try:
        url = tubeLink
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        splitTitle = soup.title.string.split(' - ')  # remove ' - Youtube' string from title
        return splitTitle[0]

    except Exception as e:
        print('err_tubeLink: ' + tubeLink)
        print(e)


# bot is ready


@client.event
async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)


@client.event  # on new message
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == client.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            print(str(message.content))
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print('@client.event' + str(e))

# start bot
client.run(token)
