# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:47:38 2019

@Author Richard Chen 
"""
import os
import discord
from discord.ext import commands
import praw
from dotenv import load_dotenv
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req

description = '''A Discord Bot to find deals from RedFlagDeals and Reddit bot searcher'''
bot = commands.Bot(command_prefix='$', description=description)

#os.environ['CLIENT_ID']
#os.environ['CLIENT_SECRET']
reddit = praw.Reddit(client_id= os.environ['CLIENT_ID'],
                     client_secret= os.environ['CLIENT_SECRET'],user_agent='RedditWebScraping')
subr = ''
client = discord.Client()
text_channel_list = []
# stores user post_listing from RFD
user_posts = []
# stores time of user_post from RFD
time = []
# used to see if a redflagdeals post is the very first post
counter = 0

#Adds a new line to every string
def join_strings(curr_string):
    return "\n".join(curr_string)

# Checks character limit of discord bot message
def exceed_char_limit(curr_string):
    if (len(curr_string)>=500):
        return True
    else:
        return False 

# Changes the url based on specified category
def category_url(url):
    if url == "all":
        return "https://forums.redflagdeals.com/hot-deals-f9/"
    elif url == "apparel":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=12"
    elif url == "automotive":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=11"
    elif url == "beauty":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=10"
    elif url == "phone":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5121"
    elif url == "computer":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=9"
    elif url == "entertainment":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=8"
    elif url == "finance":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=7"
    elif url == "groceries":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=53"
    elif url == "home":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5"
    elif url == "restaurant":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=6"
    elif url == "sports":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=3"
    elif url == "travel":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=2"
    elif url == "games":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5127"
    else: 
        return "invalid"

# Adds Header from forum 
def add_header(curr_string,counter):
    if counter == 0:
        return "__**Red Flag Deals Forum Hot Deals:**__\n\n" + curr_string+"** **"+"\n"
    else:
        return curr_string

# Finds the score of a deal
def find_score(deal,index):
    return deal[index].findAll("span", {"class": "total_count"})[0].text

# Finds retailer of a deal
def find_retailer(deal,index):
    return deal[index].findAll("a", {"class": "topictitle_retailer"})

# Finds time of a deal 
def find_time(deal,index):
    return deal[index].findAll("ul", {"class": "thread-meta-small"})[0].li.text.replace('\n', '')

# Finds the title of a deal
def find_sales(deal,index):
    return deal[index].findAll("a", {"class": "topic_title_link"})[0].text.replace('\n', '')

# Formatting and recreating the post
def create_post(deals,index,user_posts):
    score = find_score(deals, index)
    retailer = find_retailer(deals, index)
    time = find_time(deals ,index)
    sale = find_sales(deals ,index)
    # checks for an empty list
    if score == '':
        score = "+0 SCORE"
    if not retailer:
        retailer = deals[index].findAll("h3", {"class": "topictitle"})
        retailer = retailer[0].text.replace('\n', '')
        if retailer == sale and score == '':
            score = "**"+"+0 SCORE"+"**"
            user_posts.append(score + " " + time +" "+"**"+retailer+"**"+"\n")
        elif score == '':
            score = "**"+"+0 SCORE"+"**"
            user_posts.append(score+" "+time+" " +"**"+retailer+"**"+"\n")

        else:
            user_posts.append("**"+score+"**"+" " +" "+time+" " + "**" + retailer+"**"+"\n")
    elif score == '':
        retailer = retailer[0].text.replace('\n', '')
        user_posts.append(time+" " + "**"+retailer +"**"+" " + "**"+sale+"**"+"\n")
    else:
        retailer = retailer[0].text.replace('\n', '')
        user_posts.append("**"+score+"**"+" "+time+" " +"**"+retailer + "**"+" " + "**"+sale+"**"+"\n")
    print(user_posts)
    
    for i in user_posts:
        if 'Sponsored' in user_posts:
            return user_posts

    return user_posts


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    embedded = discord.Embed(title = "DealsBot is now Online!",
    description = "Most recent discounts", color = 0x738ADB)
    embedded.set_thumbnail(url = "https://miro.medium.com/max/307/1*O_-mR5b08DFAgYNE79RSzg.png")
    embedded.add_field(name = "Hot Deals", value = 'enter **$deal_categories** to view possible $hot_deals categories!')
    embedded.add_field(name = "Reddit Posts", value = 'enter **$enter_sub** and your subreddit to start browsing!')
    # for General discord servers, takes the first channel from the server
    # for guild in client.guilds:
    #    for channel in guild.channels:
    #        if channel.type == discord.ChannelType.text:
    #            text_channel_list.append(channel)

    # for friend's server
    myguild = bot.get_guild(221086855851016193)
    #mychannel = bot.get_channel(221086855851016193)
    #mychannel = bot.get_channel(660023716201365515)
    mychannel = bot.get_channel(781911970806497290)
    #other server 659095120104259626
    await mychannel.send(embed=embedded)
    # await text_channel_list[0].send('DealsBot is online! Would you like to seach the latest deals? Command prefix is **$**. To display the latest deals from redflagdeals forums use **$hot_deals**. To view the current subreddit that will be searched, enter **$current_sub**. To update the current sub, use **$enter_sub** followed by the desired subreddit separated by a space. To search the subreddit for top 10 hot posts, use **$hot_posts**')


@bot.command()
async def bot_help(ctx):
    await ctx.send('To display the latest deals from redflagdeals forums use **$hot_deals **. To view the current subreddit that will be searched, enter **$current_sub**. To update the current sub, use **$enter_sub** followed by the desired subreddit separated by a space. To search the subreddit for top 10 hot posts, use **$hot_posts**')

@bot.command()
async def deal_categories(ctx):
    embedded = discord.Embed(title = "Deal Categories",
    description = "A list of commands for $hot_deals (add the command after $hot_deals)", color = discord.Colour.red())
    embedded.set_thumbnail(url = "https://pbs.twimg.com/profile_images/1185292632353857539/It_3dBVK_400x400.jpg")
    embedded.add_field(name = "Commands", value = "all, apparel, automotive, beauty, phone, computer, entertainment, finance, groceries, home, entertainment, restaurant, sports, travel, game")
    await ctx.send(embed = embedded)
    
@bot.command()
async def hot_deals(ctx, category):
    user_posts = []
    my_url = category_url(category)
    if my_url == "invalid":
        await ctx.send("Error: invalid category")
    #Prompts user that it is fetching data
    await ctx.send("Fetching...")
    # Opening up connection, grabbing the page
    uClient = req(my_url)
    # Stores the content into a variable
    page_html = uClient.read()
    # Close the content
    uClient.close()
    # Html parser
    page_soup = soup(page_html, "html.parser")
    # Searching html with all divs with class "thread_info_title"
    deals = page_soup.findAll("div", {"class": "thread_info_title"})
    
    for index, value in enumerate(deals):
        global counter
        # user_string = add_header(join_strings(user_posts), counter)
        user_string = add_header(join_strings(user_posts), counter)

        if exceed_char_limit(user_string):
            embedded = discord.Embed(title = "Hot Deals",
            description = "Most recent discounts", color = discord.Colour.red())
            embedded.set_thumbnail(url = "https://pbs.twimg.com/profile_images/1185292632353857539/It_3dBVK_400x400.jpg")
            embedded.add_field(name = "get started", value = user_string)
            await ctx.send(embed = embedded)
            user_posts = ["\n"]
            #adds 1 to the counter 
            counter +=1

        if counter == 15:
            break 

        else:
            orig_len = len(user_posts)
            user_posts = create_post(deals,index,user_posts)
            
            if len(user_posts) == orig_len:
                counter +=0
            else:
                counter +=1
    counter = 0
    return


@bot.command()
async def enter_sub(ctx, sub: str):
    global subr
    subr = sub
    await ctx.send('Current subreddit: ' + '**'+subr+'** ')


@bot.command()
async def current_sub(ctx):
    global subr
    if subr == '':
        await ctx.send('No specified subreddit at the moment.')
    else:
        await ctx.send(subr)


@bot.command()
async def reddit_posts(ctx):
    global subr
    hot1 = reddit.subreddit(subr).hot(limit=10)
    for post in hot1:
        embedded = discord.Embed(title = subr,
        description = '__**Hot Posts from ' + subr + "**__", color = 0xFF5700)
        embedded.add_field(name = "get started", value = "** **"+"\n"+"**Upvotes: "+str(post.score)+"** " +"**"+post.title+"**"+"\n"+post.url+"\n" )
        embedded.set_image(url = post.url)
        embedded.set_thumbnail(url = "https://pbs.twimg.com/profile_images/1197561676393926656/KUZlGyLX_400x400.jpg")
        await ctx.send(embed = embedded)
# For Heroku
bot.run(os.environ['DISCORD_TOKEN'])



