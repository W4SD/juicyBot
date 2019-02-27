# bot.py
import discord
import requests
import json
import random
from bs4 import BeautifulSoup

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
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                            break
                        else:
                            return self.client.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(command['trigger'], command['args_num'], ', '.join(command['args_name'])))
                            break
                else:
                    break
            elif message.content.startswith('https://www.youtube.com/') or message.content.startswith('https://youtu.be/'):
            #elif message.content.startswith('https://'):
                return self.client.send_message(message.channel, 'Video: "{}"'.format(tubeTitler(message.content)))
                break
            else:
                break


# create discord client
client = discord.Client()
token = 'NTQ2NTAwMjk0Njg3NTg4MzUz.D1hWuQ.DCm_ba0ycd2FJ95cPJ7Nt5zIzhU'

# create the CommandHandler object and pass it the client
ch = CommandHandler(client)

## start commands command


def commands_command(message, client, args):
    try:
        count = 1
        coms = '**Commands List**\n'
        for command in ch.commands:
            coms += '{}.) {} : {}\n'.format(count,
                                            command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!commands',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints a list of all the commands!'
})
## end commands command

## start ip commad


def ip_command(message, client, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'],
                                      resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)
    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!ip',
    'function': ip_command,
    'args_num': 1,
    'args_name': ['IP\Domain'],
    'description': 'Prints information about provided IP/Domain!'
})
## end ip command

## coin flip - commit

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

## youtube link titler


def tubeTitler(tubeLink):
    try:
        print('tubeLink: ' + tubeLink)

        url = tubeLink
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup.title.string

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

# on new message
@client.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == client.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print(e)

# start bot
client.run(token)
