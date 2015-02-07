# DOC:
# http://www.zillow.com/howto/api/GetDemographics.htm
#
# EXAMPLES:
# http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1e1hgxwby17_81d4x&state=WA&city=Seattle&neighborhood=Ballard
# http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1e1hgxwby17_81d4x&state=CA&city=SF&neighborhood=Jackson+Squre

import sys
import requests

from xml.etree import ElementTree as ET

API_KEY = 'zws-id=X1-ZWz1e1hgxwby17_81d4x'
API_URL = 'http://www.zillow.com/webservice/GetDemographics.htm?%(api_key)s&state=%(state)s&city=%(city)s&neighborhood=%(neighborhood)s'

STATE = 'CA'
CITY = 'SF' # e.g. SF or Seattle
NEIGHBORHOOD_FN = 'gold/sf_nbr_names.txt'

req_count = 0
match_count = 0

with open(NEIGHBORHOOD_FN) as f:
    for line in f:
        neighborhood = line.strip()

        if len(neighborhood) == 0:
            continue

        sys.stderr.write('#%d: %s (%d)\n' % (req_count, neighborhood, match_count))
        neighborhood = neighborhood.lower()

        url = API_URL % { 'api_key': API_KEY, 'state': STATE,
            'city': CITY, 'neighborhood': neighborhood }

        r = requests.get(url)
        req_count += 1

        xml_s =  r.text.encode('utf-8')
        xml_t = ET.fromstring(xml_s)

        matched_nbr = xml_t.findtext('.//response/region/neighborhood')
        if matched_nbr is None:
            continue

        matched_nbr = matched_nbr.lower()
        if not(neighborhood in matched_nbr) and not(matched_nbr in neighborhood):
            continue

        print '%s\t%s' % (neighborhood, xml_s)
        match_count += 1
        sys.stderr.write('Found\n')

sys.stderr.write('Total requests: %d\n' % req_count)
sys.stderr.write('Total matches: %d\n' % match_count)
