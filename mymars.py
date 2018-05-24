from splinter import Browser
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import json

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)
  
def browse_url(browser,url):
    browser.visit(url)
    time.sleep(30)
    html = browser.html
    return BeautifulSoup(html, 'html.parser')

def store_in_mongo(mars_info_df):
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars
    collection = db.marsinfo
    collection.drop()
    collection.insert_many(mars_info_df.to_dict('mars_info_df'))

def get_mars_news():
        ###############GET LATEST IMAGE PUBLISHED ##############################
    browser=init_browser()
    news_results=browse_url(browser,"https://mars.nasa.gov/news")
    news_title=news_results.find_all('div', class_="content_title")[0].text
    news_p=news_results.find_all('div', class_="article_teaser_body")[0].text
    news={'title':news_title,
          'body':news_p
        }
    return news

def get_mars_featureImg():
    browser=init_browser()
    image_results=browse_url(browser,'https://www.jpl.nasa.gov/spaceimages')
    featured_image_url='https://www.jpl.nasa.gov'+image_results.find_all("div", class_="img")[0].img["src"]
    return {'featureURL':featured_image_url}

def get_mars_weather():
    ###############GET LATEST WEATHER IN MARS ##############################
    browser=init_browser()
    tweet_results=browse_url(browser,'https://twitter.com/marswxreport?lang=en')
    tweets=tweet_results.find_all("p", class_="tweet-text")
    for tweet in tweets:
        if (re.match(r'Sol \d\d\d\d', tweet.text, flags = 0)):
            mars_weather=tweet.text
            break
    return {'weather':mars_weather}


def get_mars_geo():
    ###############GET GEOGRAPHY FOR MARS ##############################
    url='https://space-facts.com/mars'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['geoparameter', 'value']
    mars_df.drop([7, 8],inplace=True)
    mars_json=json.loads(mars_df.to_json(orient='records'))
    
    return mars_json


def get_mars_hem():
    ###############GET Mars Hemisperes ##############################
    browser=init_browser()
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_results=browse_url(browser,url)
    product_items=hem_results.find_all('a',class_='product-item')
    hemisphere_image_urls=[]
    for item in product_items:
        if(item.h3):
            hem_side={}
            hem_side["title"]=item.h3.text.replace(" Enhanced","")
            browser.click_link_by_partial_text(item.h3.text)
            time.sleep(30)
            html = browser.html
            hem_detail_result= BeautifulSoup(html, 'html.parser')
            hem_side["img_url"]=hem_detail_result.find_all('div',class_='downloads')[0].ul.li.a["href"]
            hemisphere_image_urls.append(hem_side)
            browser.click_link_by_partial_text('Back')
            time.sleep(15)
    return  hemisphere_image_urls