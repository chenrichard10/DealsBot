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
#used to trakc the very first post
counter = 0


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # for General discord servers 
    '''for guild in client.guilds:
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel_list.append(channel)'''

    #for friend's server 
    channel = client.get_channel(659095120104259626)


    
    print(text_channel_list)
    await channel.send('DealsBot is online! Would you like to seach the latest deals? Send $hot deals to see the latest deals on red flag deals forum')

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

        for index,value in enumerate(deals):
            user_string = "\n".join(user_posts)
            
            if (index==0):
                continue 
            
            elif (len(user_string)) > 1800:
                global counter
                if  counter == 0:
                    user_string = "__**Red Flag Deals Forum Hot Deals:**__\n\n" +user_string+"** **"
                    await message.channel.send(user_string) 
                    user_posts = []
                    counter = 1
                    continue 
                    
                else:
                    user_string = user_string+"\n"
                    await message.channel.send(user_string)
                    user_posts= ["__**More Deals:**__\n"]
                    continue 
                    

                
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
                    if retailer == sale and score =='':
                        user_posts.append(time+" "+"**"+retailer+"**"+"\n")
                    elif score!= '':
                        user_posts.append(time+" "+"**"+retailer+"**"+"\n")
                    else:
                        user_posts.append("**"+score+"**"+" "+"**"+ retailer+"**"+" "+sale+"\n")
                elif score == '':
                    retailer = retailer[0].text.replace('\n','')
                    user_posts.append(time+" " +"**"+retailer+ "**"+" "+ "**"+sale+"**"+"\n")
                else:
                    retailer = retailer[0].text.replace('\n','')
                    user_posts.append("**"+score+"**"+" "+time+" " +"**"+retailer+ "**"+" "+ "**"+sale+"**"+"\n") 
        
        user_posts= "\n".join(user_posts)
        
        await message.channel.send(user_posts)
        return
        
        

        

client.run(TOKEN)
