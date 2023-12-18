import re
import dateparser
import urllib.parse
import requests
import datetime
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

GOOGLE_API_KEY = config['GOOGLE_API_KEY']
GOOGLE_CSE_ID_SPOTIFY = config['GOOGLE_CSE_ID_SPOTIFY']
GOOGLE_CSE_ID_IMAGE = config['GOOGLE_CSE_ID_IMAGE']


def string_to_timestamp(string, format):
    return datetime.datetime.strptime(string, format)


def parse_release_list(release_list):
    list_with_parsed_date = []
    for m in release_list:
        date = dateparser.parse(m["date"])
        m["date"] = date
        # keep only parsable date
        if date:
            list_with_parsed_date.append(m)
    unreleased_release_list = [a for a in list_with_parsed_date if a["date"]>datetime.datetime.today()]
    return unreleased_release_list


def google_search_playlists(query, n=3):
    query = urllib.parse.quote(query)
    url = f"https://customsearch.googleapis.com/customsearch/v1?cx={GOOGLE_CSE_ID_SPOTIFY}&q={query}&key={GOOGLE_API_KEY}"
    resp = requests.get(url).json()
    try:
        return [s["link"] for s in resp["items"][0:n]]
    except KeyError:
        print(f"No playlist found for {query}")
        return []


def google_search_image(query):
    query = urllib.parse.quote(query)
    url = f"https://customsearch.googleapis.com/customsearch/v1?cx={GOOGLE_CSE_ID_IMAGE}&imgSize=LARGE&imgType=photo&q={query}&searchType=image&key={GOOGLE_API_KEY}"
    resp = requests.get(url).json()
    try: 
        return resp["items"][0]["link"]
    except KeyError:
        print(f"No image found for {query}")
        return None


def url_to_id(url, type):
    if type not in ['track', 'playlist', 'album']:
        raise ValueError('Invalid type specified. Type must be one of "track", "playlist", or "album".')

    # This pattern dynamically inserts the specified type into the regular expression
    pattern = re.compile(f'{type}/([a-zA-Z0-9]+)(?:\\?|$)')
    match = pattern.search(url)

    if match:
        return match.group(1)
    else:
        raise ValueError(f'Not the right Spotify object (should be {type})')
    

def remove_items_missing_keys(dict_list, required_keys):
    """
    Remove items from a list of dictionaries that do not contain all the required keys.

    :param dict_list: List of dictionaries to filter.
    :param required_keys: List of keys that each dictionary must contain.
    :return: Filtered list of dictionaries.
    """
    return [item for item in dict_list if all(key in item for key in required_keys)]


