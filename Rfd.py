# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 17:25:42 2019

@author: chenp
"""

#Framework used to parse HTML
from bs4 import BeautifulSoup as soup
# Used to grab the URL
from urllib.request import urlopen as req
#Create a connection to the database
my_url = input('Enter $hot deals to see the latest deals on redflagdeals:')

if my_url=='$hot deals':
    my_url= 'https://forums.redflagdeals.com/hot-deals-f9/'
# Opening up connection, grabbing the page
uClient = req(my_url)
#Stores the content into a variable
page_html= uClient.read()
#Close the content 
uClient.close()
#Html parser
page_soup= soup(page_html,"html.parser")   
deals = page_soup.findAll("div",{"class":"thread_info_title"})
user_posts = []
time = []
for index, value in enumerate(deals):
    if (index==0):
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
            if retailer == sale:
                user_posts.append(score+" "+time+" "+retailer)
            else:
                user_posts.append(score+" "+ retailer+" "+sale)
        else:
            retailer = retailer[0].text.replace('\n','')
            user_posts.append(score+" "+time+" " +retailer +" "+ sale)
            
for x in user_posts:
    print(x)







    
    