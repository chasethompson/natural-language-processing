from requests import get
from bs4 import BeautifulSoup
import numpy as np
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re
import pandas as pd
from tabulate import tabulate

# ~~~~~ Acquire Data ~~~~~ #


#----------------------------#
#  Acquire Codeup Blog Data  #
#----------------------------#

urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
        'https://codeup.com/data-science-myths/',
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
        'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

def get_blog_articles(urls, cache=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cache == False which returns a df from a csv file.
    If cache == True, the function scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    '''
    if cache == False:
        df = pd.read_csv('big_blogs.csv', index_col=0)
    else:
        headers = {'User-Agent': 'Codeup Bayes Data Science'} 

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # get request to each url saved in response
            response = get(url, headers=headers)

            # Create soup object from response text and parse
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the title of each blog in variable title
            title = soup.find('h1', itemprop='headline').text

            # Save the text in each blog to variable text
            text = soup.find('div', itemprop='text').text

            # Create a dictionary holding the title and text for each blog
            article = {'title': title, 'content': text}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to csv file for faster access
        df.to_csv('big_blogs.csv')
    
    return df

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The main Codeup blog page with all the urls
    url = 'https://codeup.com/resources/#blog'
    
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # Send request to main page and get response
    response = get(url, headers=headers)
    
    # Create soup object using response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create empty list to hold the urls for all blogs
    urls = []
    
    # Create a list of the element tags that hold the href/links
    link_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    
    # get the href/link from each element tag in my list
    for link in link_list:
        
        # Add the link to my urls list
        urls.append(link['href'])
        
    return urls
#-------------------------#
#  Acquire InShorts Data  #
#-------------------------#

def get_news_articles():
    filename = 'inshorts_news_articles.csv'

    # check for presence of the file or make a new request
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()

def get_articles_from_topic(url):
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    output = []

    articles = soup.select(".news-card")

    for article in articles: 
        title = article.select("[itemprop='headline']")[0].get_text()
        body = article.select("[itemprop='articleBody']")[0].get_text()
        author = article.select(".author")[0].get_text()
        published_date = article.select(".time")[0]["content"]
        category = response.url.split("/")[-1]

        article_data = {
            'title': title,
            'body': body,
            'category': category,
            'author': author,
            'published_date': published_date,
        }
        output.append(article_data)

    return output


def make_new_request():
    urls = [
        "https://inshorts.com/en/read/business",
        "https://inshorts.com/en/read/sports",
        "https://inshorts.com/en/read/technology",
        "https://inshorts.com/en/read/entertainment"
    ]

    output = []
    
    for url in urls:
        # We use .extend in order to make a flat output list.
        output.extend(get_articles_from_topic(url))

    df = pd.DataFrame(output)
    df.to_csv('inshorts_news_articles.csv') 

    return df