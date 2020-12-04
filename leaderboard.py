import discord
import requests
from dotenv import load_dotenv
import os
from prettytable import PrettyTable



load_dotenv()
API_KEY = os.getenv('API_KEY')
session_value = os.getenv('session')
cookie={'session': session_value}

url = 'https://adventofcode.com/2020/leaderboard/private/view/1084621.json'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        try:
            response = requests.request("GET",url,cookies=cookie).json()
            message_to_client= PrettyTable(['Name', 'Stars', 'Global Score'])

            for key in response['members']:
                name = response['members'][key]['name']
                stars= response['members'][key]['stars']
                global_score = response['members'][key]['global_score']
                message_to_client.add_row([name,stars, global_score])
            await message.channel.send(message_to_client.get_string(sortby="Stars",reversesort=True))
        except:
            await message.channel.send("Could not retreive the leaderboard")
        
client.run(API_KEY)