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
                if span.text not in stop_list and len(span.text) > 3:
                    r.append(span.text)
        review_dct[website] = r

###____________________________________________________________________TO PUT IN ANALYSIS FILE________________________________________________________________###
stops = ['2 S Station', 'Boston, MA 02111', 'Yelp users haven’t asked any questions yet about Amtrak.', 'Start your review of Amtrak.']
reviews = {}

# # Scrape reviews off Yelp and add valid reviews to list
add_reviews_to_dict(0, 90, step=10, base_url='https://www.yelp.com/biz/amtrak-boston-3?start={}',
                    tag_type='span', class_names='raw__09f24__T4Ezm', stop_list=stops, review_dct=reviews)

# # Loop through each page fo Trustpilot and add valid reviews to the list
add_reviews_to_dict(1, 30, base_url="https://www.trustpilot.com/review/www.amtrak.com?page={}",
                              tag_type='p', review_dct=reviews,
                              class_names='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn',
                              stop_list=stops,
                              attrs={'data-service-review-text-typography': 'true'})

# Loop through each page fo Viewpoints.com and add valid reviews to the list
add_reviews_to_dict(0, 1, base_url="https://www.viewpoints.com/Amtrak-Train-TRavel-reviews",
                              tag_type='p', review_dct=reviews,
                              class_names=['pr-review-faceoff-review', 'pr-comments', 'pr-review-faceoff-review-full'],
                              stop_list=stops)

# Loop through each page fo Reddit.com and add valid reviews to the list
add_reviews_to_dict(0, 1, base_url="https://www.sitejabber.com/reviews/amtrak.com",
                              tag_type='p', review_dct=reviews,
                              stop_list=stops)


# Get review data statistics
print_review_count(review_dict=reviews)