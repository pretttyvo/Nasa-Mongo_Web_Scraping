from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/prettyvo/Downloads/chromedriver2"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # collect all data into a single dictionary
    mars_data = {}
    # NASA MARS NEWS
    # connect browser to url and parse data images of the titles and summaries
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)
    html = browser.html
    mars_news = BeautifulSoup(html, 'html.parser')
    # titles
    headlines = mars_news.find_all('div', class_='content_title')
    titles = [headline.text.strip() for headline in headlines][0]
    # summary data
    details = mars_news.find_all('div', class_='article_teaser_body')
    summary = [detail.text.strip() for detail in details][0]

    # JPL SPACE IMAGES
    # connect browser to url and parse data for image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    html = browser.html
    mars_jpl_image = BeautifulSoup(html, 'html.parser')
    # collect the link for the image
    images = mars_jpl_image.find_all('div', class_='default floating_text_area ms-layer')
    img = [image.a['data-fancybox-href'] for image in images]
    featured_image_url = "https://www.jpl.nasa.gov" + img[0]

    # SPACE WEATHER
    # connect browser to url and parse data for tweet
    mars_tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_tweet_url)
    html = browser.html
    mars_twitter = BeautifulSoup(html, 'html.parser')
    # get data
    tweets = mars_twitter.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = [tweet.text for tweet in tweets][0]

    #MARS FACTS
    # connect browser to url and parse data for tweet
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html = browser.html
    mars_facts = BeautifulSoup(html, 'html.parser')
    facts = mars_facts.find_all('table', id='tablepress-mars')
    table = [fact.text for fact in facts]
    data = list(filter(None, table[0].split('\n')))
    result = []

    for i in range(0,9):
        separated = data[i].split(':')
        results = ({
            'Physical' : separated[0],
            'Data' :separated[1]
        })
        result.append(results)
    df = pd.DataFrame(result)
    df = df[['Physical', 'Data']].set_index(['Physical'])
    mars_facts_table =  df.to_html().strip()

    
    # MARS HEMISPHERES
    # connect browser to url and parse data images of the hemisphere
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    html = browser.html
    mars_hemisphere = BeautifulSoup(html, 'html.parser')
    hemisphere_imgs = mars_hemisphere.find_all('div', class_='description')
    img_link = [img.a['href'] for img in hemisphere_imgs]
    hem_title = [img.a.text for img in hemisphere_imgs]
    hemisphere_image_urls = []
    for j in range(0,4):
        
        res_link = 'https://astrogeology.usgs.gov/' + img_link[j]
        browser.visit(res_link)
        res_hemisphere = BeautifulSoup(browser.html, 'html.parser')
        hemispheres = res_hemisphere.find_all('div', class_='downloads')
        img_url = [hemisphere.a['href'] for hemisphere in hemispheres]
        hemisphere_image_dict = ({
            'title': hem_title[j],
            'img_url': img_url[0]
        })
        hemisphere_image_urls.append(hemisphere_image_dict)
    
    
    # news headline
    mars_data['news_headline'] = titles
    mars_data['news_summary'] = summary
    # JPL featured photo
    mars_data['featured_image_url'] = featured_image_url
    # mars facts
    mars_data['mars_table'] = mars_facts_table
    #mars weather
    mars_data['mars_weather'] = mars_weather
    # mars hemispheres
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return(mars_data)

if __name__ == "__main__":

    print(featured_image_url)
