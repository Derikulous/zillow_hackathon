import json
import requests

query = 'Capitol Hill, Seattle'
url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s&start=0' % query.replace(' ', '+'))

response = requests.get(url)

image_res = json.loads(response.text)
data = image_res['responseData']['results']

for myUrl in data:
    print myUrl['unescapedUrl']
