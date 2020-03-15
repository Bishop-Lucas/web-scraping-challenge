from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time 

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    soup = bs(html, "html.parser")

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(news_title)
    print(news_p)
    return news_title, news_p


def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
   
    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, "html.parser")

    # Retrieve background-image url from style tag 
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = "https://www.jpl.nasa.gov"

    # Concatenate website url with scrapped route
    image_url = main_url + image_url

    # Display full link to featured image
    image_url
    
    return img_url


def hemispheres(browser):

    # A way to break up long strings
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(hemispheres_url)
    #write your code here
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls     
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

    # Display hemisphere_image_urls
    hemisphere_image_urls
    return hemisphere_image_urls


def twitter_weather(browser):
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)
    #write your code here
    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass
    return mars_weather




def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    # Add some bootstrap styling to <table>
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
