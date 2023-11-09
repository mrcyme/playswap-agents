from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyBqXy3c5wVL0U147TMfmYZ52Dceb8m62KU"
my_cse_id = "91587380115664474"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    print(res)
    return res['items']

results = google_search(
    'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)
for result in results:
    pprint.pprint(result)