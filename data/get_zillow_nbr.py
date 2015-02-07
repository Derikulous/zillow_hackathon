# DOC:
# http://www.zillow.com/howto/api/GetDemographics.htm
#
# EXAMPLE:
# http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1e1hgxwby17_81d4x&state=WA&city=Seattle&neighborhood=Ballard

import sys
import requests

API_KEY = 'zws-id=X1-ZWz1e1hgxwby17_81d4x'
API_URL = 'http://www.zillow.com/webservice/GetDemographics.htm?%(api_key)s&state=%(state)s&city=%(city)s&neighborhood=%(neighborhood)s'

STATE = 'CA'
CITY = 'San Fransisco'
NEIGHBORHOOD_FN = 'gold/sf_nbr_names.txt'

with open(NEIGHBORHOOD_FN) as f:
    count = 0
    for line in f:
        neighborhood = line.strip()
        if len(neighborhood) == 0:
            continue

        sys.stderr.write('#%d: %s\n' % (count, neighborhood))
        neighborhood = neighborhood.lower()

        url = API_URL % { 'api_key': API_KEY, 'state': STATE,
            'city': CITY, 'neighborhood': neighborhood }

        r = requests.get(url)
        xml = r.text.encode('utf-8')
        count += 1

        print '%s\t%s' % (neighborhood.lower(), xml)

