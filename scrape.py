from bs4 import BeautifulSoup
import requests
from pprint import pprint

def get_all_tags(url, tag_type, class_=None):
    """Returns a list of all requested tags

    Args:
      url (String): URL of website
      tag_type (String): Type of tag to search and return

    Return:
      tags (bs4.ResultSet): List of tags
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')

        if class_ is not None:
            tags = soup.find_all(tag_type, class_=class_)

        else:
            tags = soup.find_all(tag_type)

        return tags

    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

# Scrape reviews off Yelp and add valid reviews to list
reviews = []
stops = ['2 S Station', 'Boston, MA 02111', 'Yelp users haven’t asked any questions yet about Amtrak.', 'Start your review of Amtrak.']

# Loop through each page of Yelp and add valid reviews to the list
for i in range(0,90,10):
    result = get_all_tags(url=f'https://www.yelp.com/biz/amtrak-boston-3?start={i}', tag_type='span', class_='raw__09f24__T4Ezm')
    if result:
        for span in result:
            if span.text not in stops:
                reviews.append(span.text)

# Loop through each page fo TravelAdvisor and add valid reviews to the list
k = []
for i in range(1,30):
    result = get_all_tags(url=f'https://www.trustpilot.com/review/www.amtrak.com?page={i}', tag_type='p',
             class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn')
    if result:
        for span in result:
            if span.text not in stops:
                reviews.append(span.text)

print(len(reviews))