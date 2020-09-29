#!/usr/bin/env python
# coding: utf-8

# In[24]:


# Dependencies & Setup
from splinter import browser 
from bs4 import BeautifulSoup as bs
import pandas as pd
import time 
import os


# In[25]:


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# In[26]:


# NASA Mars News
browser = init_browser()

# NASA Mars News Site
url = "https://mars.nasa.gov/news/"
browser.visit(url)

time.sleep(3)

# Scrape Page
html = browser.html
soup = bs(html, "html.parser")

# News
news = soup.find_all('div', class_="list_text")[0]

# Title
news_title = news.find(class_="content_title").text

# News Article
news_p = news.find(class_="article_teaser_body").text

# Date
news_date = news.find(class_='list_date').text

# Store As Dictionary
news_data= {
    "News Date": news_date,
    "News Title": news_title,
    "News Paragraph" : news_p
}
    
      
browser.quit()


# In[28]:


# JPL Mars Space Images - Featured Image
browser = init_browser()

# JPL Site
url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_jpl)

time.sleep(3)

# Scrape Page
html= browser.html
soup= bs(html, "html.parser")

 # Featured Image
featured_image = soup.find('article', class_="carousel_item")['style']

# Image Name 
featured_image_name= (featured_image.split("wallpaper/")[1]).split(".jpg")[0]

# Image URL Creation
jpl_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg"
image_url= jpl_url + featured_image_name + ".jpg"


browser.quit()


# In[30]:


# Mars Facts
url_facts ="https://space-facts.com/mars/"

# Fact Table 
table = pd.read_html(url_facts)
fact_table = pd.DataFrame(table[0])

fact_table = fact_table.rename(columns={
    0 : "Description",
    1 : "Value"
})

fact_table.set_index("Description", inplace = True)

# Table to HTML
table_html = fact_table.to_html()
table_html= table_html.replace('\n',"")


# In[31]:


# Mars Hemisphere
browser = init_browser()

# Scrape Mars Hemispheres
hemisphere_url = "https://astrogeology.usgs.gov"
hemisphere_img = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemisphere_img)

time.sleep(3)

# Scrape Page
html= browser.html
soup= bs(html, "html.parser")

# URL
url_list= []
for x in range (8):
    if (x % 2) == 0:
        url_img = soup.find('div', class_="collapsible results").find_all('a')[x]['href']
        url_full = hemisphere_url + url_img
        url_list.append(url_full)

browser.quit()


# In[32]:


# Title & URLs
hemisphere_url = "https://astrogeology.usgs.gov"

final_output = []

# URL & Title 
for url in url_list:
    browser = init_browser()
    browser.visit(url)

    time.sleep (3)

    # Scrape Page
    html = browser.html
    soup = bs(html, "html.parser")

    # URL of Each Image 
    src_image = soup.find('img', class_="wide-image")['src']
    final_image = hemisphere_url + src_image

    # Title of Each Image 
    title_of_image = soup.find('h2', class_="title").get_text()

    # Dictionary 
    dic = {"Title": title_of_image ,
          "Image_URL": final_image}

    final_output.append(dic)

    browser.quit()


# In[37]:


# Last Dictionary Containing All Discovered Info.
hemisphere_image_urls = {
    "News Date": news_date,
    "News Title": news_title,
    "News Paragraph": news_p,
    "Featured Image URL": image_url,
    "Fact Table": table_html,
    "Hemisphere_Image_Title_1": final_output[0]["Title"],
    "Hemisphere_Image_URL_1": final_output[0]["Image_URL"],
    "Hemisphere_Image_Title_2": final_output[1]["Title"],
    "Hemisphere_Image_URL_2": final_output[1]["Image_URL"],
    "Hemisphere_Image_Title_3": final_output[2]["Title"],
    "Hemisphere_Image_URL_3": final_output[2]["Image_URL"],
    "Hemisphere_Image_Title_4": final_output[3]["Title"],
    "Hemisphere_Image_URL_4": final_output[3]["Image_URL"] 
}


# In[38]:


print(hemisphere_image_urls)

