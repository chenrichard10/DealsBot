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

description = '''A redflagdeals discord bot'''
bot = commands.Bot(command_prefix='$', description=description)

reddit = praw.Reddit(client_id='OtBVnyEJ_YCE-g',
                     client_secret='x9Lq_Nk4XnX1tSbZ7_vVrJ5U3ck', user_agent='RedditWebScraping')
subr = ''
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()
text_channel_list = []
# stores user post_listing from RFD
user_posts = []
# stores time of user_post from RFD
time = []
# used to see if a redflagdeals post is the very first post
counter = 0

#Adds a new line to eveyr string
def join_strings(curr_string):
    return "\n".join(curr_string)

# Checks character limit of discord bot message
def exceed_char_limit(curr_string):
    if (len(curr_string)>=1800):
        return True
    else:
        return False 

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
    score = find_score(deals,index)
    retailer = find_retailer(deals,index)
    time = find_time(deals,index)
    sale = find_sales(deals,index)
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
    return user_posts


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # for General discord servers, takes the first channel from the server
    '''for guild in client.guilds:
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel_list.append(channel)'''

    # for friend's server
    mychannel = bot.get_channel(659095120104259626)

    # await mychannel.send('DealsBot is online! Would you like to seach the latest deals? Send $hot deals to see the latest deals on red flag deals forum')
    await mychannel.send('DealsBot is online! Would you like to seach the latest deals? Command prefix is **$**. To display the latest deals from redflagdeals forums use **$hot_deals**. To view the current subreddit that will be searched, enter **$current_sub**. To update the current sub, use **$enter_sub** followed by the desired subreddit separated by a space. To search the subreddit for top 10 hot posts, use **$hot_posts**')


@bot.command()
async def bot_help(ctx):
    await ctx.send('To display the latest deals from redflagdeals forums use **$hot_deals**. To view the current subreddit that will be searched, enter **$current_sub**. To update the current sub, use **$enter_sub** followed by the desired subreddit separated by a space. To search the subreddit for top 10 hot posts, use **$hot_posts**')


@bot.command()
async def hot_deals(ctx):
    user_posts = []
    my_url = "https://forums.redflagdeals.com/hot-deals-f9/"
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
        user_string = add_header(join_strings(user_posts), counter)

        if (index == 0):
            continue

        elif exceed_char_limit(user_string):
            await ctx.send(user_string)
            user_posts = ["\n"]
            #adds 1 to the counter 
            counter +=1;
            continue

        else:
            user_posts = create_post(deals,index,user_posts)

    user_posts = join_strings(user_posts)
    await ctx.send(user_posts)
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
async def hot_posts(ctx):
    global subr
    #a = []
    hot1 = reddit.subreddit(subr).hot(limit=10)
    await ctx.send('__**Hot Posts from ' + subr + "**__"+ "** **"+"\n" )
    for post in hot1:
        await ctx.send("** **"+"\n"+"**Upvotes: "+str(post.score)+"** " +"**"+post.title+"**"+"\n"+post.url+"\n" )

bot.run(TOKEN)
