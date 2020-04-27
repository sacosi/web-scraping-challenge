# importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime

sleep_time=5

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    scrape_dict={}

    #### NASA Mars News ####

    browser = init_browser()
    
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(sleep_time)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('div',class_="list_text")

    news_title = article.find('div',class_='content_title').text
    news_p = article.find('div',class_='article_teaser_body').text

    browser.quit()
    # print(f'{news_title}')
    # print('---')
    # print(f'{news_p}')

    scrape_dict['Latest_News']=news_title
    scrape_dict['News_p']=news_p


    #### PL Mars Space Images - Featured Image ####

    browser = init_browser()

    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(sleep_time)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(sleep_time)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image=soup.find('img',class_='fancybox-image')
    image_url=image['src']
    featured_image_url=f'https://www.jpl.nasa.gov{image_url}'

    browser.quit()

    # print(featured_image_url)

    scrape_dict['Space_Image']=featured_image_url


    #### Mars Weather ####

    browser = init_browser()

    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(sleep_time)

    html = browser.html

    soup = BeautifulSoup(html,'html.parser')
    articles=soup.find_all('span')

    for article in articles:
        if "InSight" in article.text:
            mars_weather = article.text
            break

    browser.quit()

    # print(mars_weather)

    scrape_dict['Weather']=mars_weather


    #### Mars Facts ####

    url='https://space-facts.com/mars/'

    tables = pd.read_html(url)

    df=tables[0]
    df=df.rename(columns={0:"Description",1:'Value'})
    df=df.set_index('Description')

    mars_facts_html=df.to_html()

    scrape_dict['Facts_table']=mars_facts_html


    #### Mars Hemispheres ####

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = init_browser()

    browser.visit(url)
    time.sleep(sleep_time)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        titles_link=soup.find_all('h3')
    except:
        print("An exception occurred")

    hemisphere_image_urls=[]
    for title in titles_link:
        try:
            browser.click_link_by_partial_text(title.text)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            img=soup.find('div',class_='downloads').a['href']
            hiu={
                'title':title.text,
                'img_url':img
            }
            hemisphere_image_urls.append(hiu)
            browser.back()
        except:
            print("An exception occurred")

    browser.quit()

    hemisphere_image_urls

    scrape_dict['Hemispheres']=hemisphere_image_urls

    #Storing Last Update
    now = datetime.now()
    scrape_dict['timestamp']=now.strftime("%m/%d/%Y-%H:%M")

    return scrape_dict

#     print(scrape_dict)

# scrape()