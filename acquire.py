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

def get_soup(link):
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(link, headers=headers)

    return BeautifulSoup(response.content, 'html.parser')

def get_article_content(soup):
    article_text = soup.find('div', class_='jupiterx-post-content clearfix').text
    article_title = soup.find('h1', class_='jupiterx-post-title').text

    return {'title': article_title,
            'content': article_text}

def get_blog_articles():
    links = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
    'https://codeup.com/data-science-myths/',
    'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
    'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
    'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

    articles = []

    for link in links:
        soup = get_soup(link)

        article_dictionary = get_article_content(soup)

        articles.append(article_dictionary)

        return articles

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