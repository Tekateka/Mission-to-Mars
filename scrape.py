# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    
    data = {
        "title": news_title,
        "paragraph": news_paragraph,
        "image": image(browser),
        "facts": facts(),
        "hemispheres": hemis(browser),
        "last_modified": dt.datetime.now()
    } 
     
    browser.quit()
    return data
        
def mars_news(browser):
    browser.visit('https://data-class-mars.s3.amazonaws.com/Mars/index.html')
    news_title = browser.find_by_css('div.content_title').text
    news_p = browser.find_by_css('div.article_teaser_body').text
    return news_title, news_p

def image(browser):
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.find_by_tag('button')[1].click()
    return browser.find_by_css('img.fancybox-image')['src']

def facts():
    return pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html',header=0,index_col=0)[0].to_html(classes="table table-striped")

def hemis(browser):
    browser.visit('https://marshemispheres.com/')
    hemispheres = []
    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['url'] = browser.find_by_text("Sample")["href"]
        browser.back()
        hemispheres.append(hemisphere)
    return hemispheres