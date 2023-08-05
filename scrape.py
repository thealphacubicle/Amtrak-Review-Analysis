from bs4 import BeautifulSoup
import requests
import re

def get_all_tags(url, tag_type, class_names=None, attrs_=None):
    """Returns a list of all requested tags

    Args:
      url (String): URL of website
      tag_type (String): Type of tag to search and return
      class_names (List): List of classes to filter through
      attrs_ (Dict): Dictionary of attributes with keys and states

    Return:
      tags (bs4.ResultSet): List of tags
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')

        if class_names is None or attrs_ is None:
            tags = soup.find_all(tag_type)

        else:
            tags = soup.find_all(tag_type, class_=class_names, attrs=attrs_)

        return tags

    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

def get_website_name(url):
    website_name = re.search(r'://(?:www\.)?([^/]+)', url).group(1)
    return website_name

def print_review_count(review_dict):
    for key, value in review_dict.items():
        print(key, f"Number of Reviews: {len(value)}")

def add_reviews_to_dict(start, end, base_url, tag_type, review_dct, class_names=None, attrs=None, stop_list = None, step=1):
    # Initial checks
    if stop_list is None:
        stop_list = ['']

    # Set default variables
    r = []
    website = get_website_name(base_url)

    # Loop through web pages and collect all tags
    for i in range(start, end, step):
        result = get_all_tags(url=base_url.format(i), tag_type=tag_type,
                              class_names=class_names, attrs_=attrs)
        if result:
            for span in result:
                if span.text not in stop_list and len(span.text.split()) > 7:
                    r.append(span.text)
        review_dct[website] = r

