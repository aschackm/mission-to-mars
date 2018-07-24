
# Mission to Mars - Scraping the Web for Information on Mars


```python
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import cssutils
import tweepy
import pandas as pd
import time
from config import consumer_key, consumer_secret, access_token, access_token_secret, weather_api_key
```


```python
# Function to initialize Splinter browser
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
```


```python
# URL of page to be scraped
nasa_url = 'https://mars.nasa.gov/news/'
# Starting Splinter and parsing site
browser = init_browser()
browser.visit(nasa_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
```


```python
# Scraping latest article and storing to variables
latest_article = soup.find("div", "list_text")
news_title = latest_article.find("div", class_="content_title").text
news_p = latest_article.find("div", class_="article_teaser_body").text
print(news_title)
print(news_p)
```

    'Storm Chasers' on Mars Searching for Dusty Secrets
    Scientists with NASA's Mars orbiters have been waiting years for an event like the current Mars global dust storm.



```python
# Navigating to JPL site
jpl_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)
```


```python
# Scraping JPL Mars site for featured image
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
carousel = soup.find('div', class_= 'carousel_items')
div_style = carousel.find('article')['style']
style = cssutils.parseStyle(div_style)
partial_url = style['background-image']
print(partial_url)
```

    url(/spaceimages/images/wallpaper/PIA18907-1920x1200.jpg)



```python
# Cleaning up image url
partial_url = partial_url.replace('url(', '').replace(')', '')
featured_image_url = "https://jpl.nasa.gov" + partial_url
print(featured_image_url)
```

    https://jpl.nasa.gov/spaceimages/images/wallpaper/PIA18907-1920x1200.jpg



```python
# Navigating to Twitter
tweet_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(tweet_url)
```


```python
# Pulling latest tweet from @marswxreport
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
mars_weather = soup.find("p", class_="tweet-text").text
print(mars_weather)
```

    L-2 years. #Mars2020



```python
# Navigating to Mars facts site
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
```


```python
# Using pandas to scrape table
facts = pd.read_html(facts_url)
print(facts)
```

    [                      0                              1
    0  Equatorial Diameter:                       6,792 km
    1       Polar Diameter:                       6,752 km
    2                 Mass:  6.42 x 10^23 kg (10.7% Earth)
    3                Moons:            2 (Phobos & Deimos)
    4       Orbit Distance:       227,943,824 km (1.52 AU)
    5         Orbit Period:           687 days (1.9 years)
    6  Surface Temperature:                  -153 to 20 °C
    7         First Record:              2nd millennium BC
    8          Recorded By:           Egyptian astronomers]



```python
# Isolating df from list and minor clean-up
facts_df = pd.DataFrame(facts[0])
facts_df.columns=['Fact','Result']
facts_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Fact</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Writing df to html table
mars_table = facts_df.to_html(index=False, justify='left', classes='mars-table')
mars_table = mars_table.replace('\n', ' ')
mars_table
```




    '<table border="1" class="dataframe mars-table">   <thead>     <tr style="text-align: left;">       <th>Fact</th>       <th>Result</th>     </tr>   </thead>   <tbody>     <tr>       <td>Equatorial Diameter:</td>       <td>6,792 km</td>     </tr>     <tr>       <td>Polar Diameter:</td>       <td>6,752 km</td>     </tr>     <tr>       <td>Mass:</td>       <td>6.42 x 10^23 kg (10.7% Earth)</td>     </tr>     <tr>       <td>Moons:</td>       <td>2 (Phobos &amp; Deimos)</td>     </tr>     <tr>       <td>Orbit Distance:</td>       <td>227,943,824 km (1.52 AU)</td>     </tr>     <tr>       <td>Orbit Period:</td>       <td>687 days (1.9 years)</td>     </tr>     <tr>       <td>Surface Temperature:</td>       <td>-153 to 20 °C</td>     </tr>     <tr>       <td>First Record:</td>       <td>2nd millennium BC</td>     </tr>     <tr>       <td>Recorded By:</td>       <td>Egyptian astronomers</td>     </tr>   </tbody> </table>'




```python
# Navigating to hemisphere image site
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)
```


```python
# Loop to scrape image info with time delay to account for browser navigation
hemisphere_image_urls = []

for i in range (4):
    time.sleep(10)
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    partial_url = soup.find("img", class_="wide-image")["src"]
    image_title = soup.find("h2",class_="title").text
    image_url = 'https://astrogeology.usgs.gov'+ partial_url
    image_dict = {"title":image_title,"image_url":image_url}
    hemisphere_image_urls.append(image_dict)
    browser.back()
    
hemisphere_image_urls
```




    [{'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]




```python
browser.quit
```
