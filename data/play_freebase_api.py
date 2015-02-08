import requests
import json
from pprint import pprint

FILTER = 'filter=(all alias:"lower queen anne, Seattle" type:/location/neighborhood)&output=(description geocode)&limit=1'
URL = 'https://www.googleapis.com/freebase/v1/search?%s' % FILTER

print URL

res = requests.get(URL)
j = json.loads(res.text)

pprint(j)



