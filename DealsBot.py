# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:47:38 2019

@author: chenp
"""
import os 
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as req


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()
text_channel_list = []
user_posts = []
time = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel_list.append(channel)
    
    print(text_channel_list)
    await (text_channel_list[0]).send('DealsBot is online! Would you like to seach the latest deals? Send $hotdeals to see the latest deals on red flag deals forum')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('**Hello!**')
        return 

    if message.content.startswith('$hot deals'):
        user_posts=[]
        my_url= "https://forums.redflagdeals.com/hot-deals-f9/" 
        # Opening up connection, grabbing the page
        uClient = req(my_url)
        #Stores the content into a variable
        page_html= uClient.read()
        #Close the content 
        uClient.close()
        #Html parser
        page_soup= soup(page_html,"html.parser") 
        deals = page_soup.findAll("div",{"class":"thread_info_title"}) 
        for index, value in enumerate(deals):
            if (index==0):
                continue 

            if (index>13):
                break
        
    
            else:
                score = deals[index].findAll("span",{"class":"total_count"})
                score = score[0].text
                retailer = deals[index].findAll("a",{"class":"topictitle_retailer"})
                time = deals[index].findAll("ul",{"class":"thread-meta-small"})
                time = time[0].li.text.replace('\n','')
                sale = deals[index].findAll("a",{"class":"topic_title_link"}) 
                sale = sale[0].text.replace('\n','')
                #checks for an empty list 
                if not retailer:
                    retailer = deals[index].findAll("h3",{"class":"topictitle"})
                    retailer = retailer[0].text.replace('\n','')
                    if retailer == sale:
                        user_posts.append("**"+score+"**"+" "+time+" "+"**"+retailer+"**")
                    else:
                        user_posts.append("**"+score+"**"+" "+"**"+ retailer+"**"+" "+sale)
                else:
                    retailer = retailer[0].text.replace('\n','')
                    user_posts.append("**"+score+"**"+" "+time+" " +"**"+retailer+ "**"+" "+ "**"+sale+"**") 
        
        user_posts= "\n".join(user_posts)
        
        await message.channel.send(user_posts)
        return
        
        

        

client.run(TOKEN)
