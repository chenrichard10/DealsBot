# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:47:38 2019

@author: chenp
"""
import os 
import discord
from discord.ext import commands
import praw 
from dotenv import load_dotenv
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as req


reddit = praw.Reddit(client_id='OtBVnyEJ_YCE-g', client_secret='x9Lq_Nk4XnX1tSbZ7_vVrJ5U3ck', user_agent='RedditWebScraping')
subreddit=''
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()
text_channel_list = []
user_posts = []
time = []
hot_posts = []
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
    mychannel = client.get_channel(659095120104259626)


    
    print(text_channel_list)
    #await mychannel.send('DealsBot is online! Would you like to seach the latest deals? Send $hot deals to see the latest deals on red flag deals forum')
    await mychannel.send('DealsBot is online! Would you like to seach the latest deals? Send $hot deals to see the latest deals on red flag deals forum'
                        +'\nSend $currentsub to view current subreddit, $entersub to change the subreddit, and $hotposts to see 10 hot posts')
@client.event
async def on_message(message):
    if message.author == client.user:
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
        # Searching html with all divs with class "thread_info_title"
        deals = page_soup.findAll("div",{"class":"thread_info_title"}) 

        for index,value in enumerate(deals):
            user_string = "\n".join(user_posts)
            
            if (index==0):
                continue 
            
            elif (len(user_string)) > 1800:
                global counter
                if  counter == 0:
                    user_string = "__**Red Flag Deals Forum Hot Deals:**__\n\n" +user_string+"** **"+"\n"
                    await message.channel.send(user_string) 
                    user_posts = ["\n"]
                    counter = 1
                    continue 
                    
                else:
                    user_string = user_string+"\n"
                    await message.channel.send(user_string)
                    user_posts= ["\n"]
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
                if score == '':
                    score = "+0 SCORE"
                if not retailer:
                    retailer = deals[index].findAll("h3",{"class":"topictitle"})
                    retailer = retailer[0].text.replace('\n','')
                    if retailer == sale and score =='':
                        score = "**"+"+0 SCORE"+"**"
                        user_posts.append(score + " "+ time+" "+"**"+retailer+"**"+"\n")
                    elif score== '':
                        score = "**"+"+0 SCORE"+"**"
                        user_posts.append(score+" "+time+" "+"**"+retailer+"**"+"\n")
                    #elif retailer == sale:
                    #    user_posts.append("**"+score+"**"+" "+" "+time+" " +"**"+ retailer+"**"+"\n")
                    else:
                        user_posts.append("**"+score+"**"+" "+" "+time+" " +"**"+ retailer+"**"+"\n")
                elif score == '':
                    retailer = retailer[0].text.replace('\n','')
                    user_posts.append(time+" " +"**"+retailer+ "**"+" "+ "**"+sale+"**"+"\n")
                else:
                    retailer = retailer[0].text.replace('\n','')
                    user_posts.append("**"+score+"**"+" "+time+" " +"**"+retailer+ "**"+" "+ "**"+sale+"**"+"\n") 
        
        user_posts= "\n".join(user_posts)
        
        await message.channel.send(user_posts)
        counter = 0
        return
    
    elif message.content.startswith('$currentsub'):
        global subreddit
        global hot_posts
        if subreddit=='':
            await message.channel.send('no specified subreddit at the moment.')
        else:
            await message.channel.send(subreddit)
    elif message.content.startswith('$entersub'):
        await message.channel.send('Please enter your subreddit')

        def check(m):
            return m.content
        subreddit = await client.wait_for('message',check=check)
        if subreddit:
            subreddit= subreddit.content
            hot_posts = reddit.subreddit(subreddit).hot(limit=10)
            for post in hot_posts:
                hot_posts.append("**Upvotes:"+str(post.score)+"** "+"**"+post.title+"**"+"\n")
            hot_posts= "\n".join(hot_posts)
            await message.channel.send(hot_posts)
client.run(TOKEN)
