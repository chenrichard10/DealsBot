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


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # for General discord servers, takes the first channel from the server
    '''for guild in client.guilds:
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                text_channel_list.append(channel)'''

    # for friend's server
    mychannel = bot.get_channel(649883813513527296)

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
        user_string = "\n".join(user_posts)

        if (index == 0):
            continue

        elif (len(user_string)) > 1800:
            global counter
            if counter == 0:
                user_string = "__**Red Flag Deals Forum Hot Deals:**__\n\n" + user_string+"** **"+"\n"
                await ctx.send(user_string)
                user_posts = ["\n"]
                counter = 1
                continue

            else:
                user_string = user_string+"\n"
                await ctx.send(user_string)
                user_posts = ["\n"]
                continue

        else:
            score = deals[index].findAll("span", {"class": "total_count"})
            score = score[0].text
            retailer = deals[index].findAll(
                "a", {"class": "topictitle_retailer"})
            time = deals[index].findAll("ul", {"class": "thread-meta-small"})
            time = time[0].li.text.replace('\n', '')
            sale = deals[index].findAll("a", {"class": "topic_title_link"})
            sale = sale[0].text.replace('\n', '')
            # checks for an empty list
            if score == '':
                score = "+0 SCORE"
            if not retailer:
                retailer = deals[index].findAll("h3", {"class": "topictitle"})
                retailer = retailer[0].text.replace('\n', '')
                if retailer == sale and score == '':
                    score = "**"+"+0 SCORE"+"**"
                    user_posts.append(score + " " + time +
                                      " "+"**"+retailer+"**"+"\n")
                elif score == '':
                    score = "**"+"+0 SCORE"+"**"
                    user_posts.append(score+" "+time+" " +
                                      "**"+retailer+"**"+"\n")

                else:
                    user_posts.append("**"+score+"**"+" " +
                                      " "+time+" " + "**" + retailer+"**"+"\n")
            elif score == '':
                retailer = retailer[0].text.replace('\n', '')
                user_posts.append(time+" " + "**"+retailer +
                                  "**"+" " + "**"+sale+"**"+"\n")
            else:
                retailer = retailer[0].text.replace('\n', '')
                user_posts.append("**"+score+"**"+" "+time+" " +
                                  "**"+retailer + "**"+" " + "**"+sale+"**"+"\n")

    user_posts = "\n".join(user_posts)

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
    a = []
    hot1 = reddit.subreddit(subr).hot(limit=10)
    for post in hot1:
        a.append("**Upvotes: "+str(post.score)+"** " +
                 "**"+post.title+"**"+"\n"+post.url+"\n")

    a = "\n".join(a)
    a = '__**Hot Posts from ' + subr + '**__\n\n' + a
    await ctx.send(a)

bot.run('NjU3NzA0NTg4MDIyOTA2OTEw.XgPKwA.o3QJ24HIHU4Ifn7k9FM40Z3FIkk')
