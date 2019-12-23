# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:47:38 2019

@author: chenp
"""
import os 
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()
text_channel_list = []


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel_list.append(channel)
    
    print(text_channel_list)
    await (text_channel_list[0]).send('DealsBot is online! Would you like to seach the latest deals? Send $hotdeals to see the latest deals on redflagdealsforum')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        return 
        

client.run(TOKEN)
