import os
import json

from pprint import pprint
from data.parsers import *

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

################################################################################
# Neighborhood data
################################################################################

class Neighborhood:
  @staticmethod
  def get_for_city_and_neighborhood(city, neighborhood):
    if city == 'SF':
      city = 'San Francisco'

    for n in Neighborhood.get_neighborhoods_in_city(city):
      if n.name.lower() == neighborhood.lower():
        return n

    raise KeyError("Did not find neighborhood %s in city %s" % (neighborhood, city))

  @staticmethod
  def get_neighborhoods_in_city(city):
    for n in Neighborhood.get_neighborhoods():
      if n.city.lower() == city.lower():
        yield n

  @staticmethod
  def get_neighborhoods():
    with open(os.path.join(SCRIPT_DIR, '../data/output/nbr_zillow_clean.tsv')) as f:
      for l in f:
        parts = l.split('\t')
        yield Neighborhood(json.loads(parts[3]))

  def __init__(self, data):
    self.data = data

  @property
  def name(self):
    return self.data['name']

  @property
  def city(self):
    return self.data['city']

  @property
  def lat_lng(self):
    return [self.data['lat'], self.data['lng']]

  @property
  def median_income(self):
    return self.data['num_attrs']['median_income']

  @property
  def median_age(self):
    return self.data['num_attrs']['median_age']

  @property
  def zillow_listings_url(self):
    return self.data['zillow_listings_url']

  @property
  def charts(self):
    return zip(self.data['charts_names'], self.data['charts_urls'])

  @property
  def description(self):
    # TODO: these come from wikipedia
    if self.name == 'Capitol Hill':
      return "Capitol Hill is a densely populated residential district in Seattle, Washington, United States. It is one of the city's most prominent nightlife and entertainment districts, and the center of the city's gay and counterculture communities."
    if self.name == 'Wallingford':
      return "Wallingford is a neighborhood in north central Seattle, Washington, named after John Noble Wallingford, Jr. Major annual events in the neighborhood include the Wallingford Kiddie Parade as part of Seafair, the Wallingford Wurst Festival run by St Benedict's Church, and the Family Fourth fireworks show at Gas Works Park. Smaller events include Seattle Tilth's chicken coop tour and the Wallingford Neighborhood office's garden and home tours."
    if self.name == 'Fremont':
      return "Fremont is a neighborhood in Seattle, Washington. Originally a separate city, it was annexed to Seattle in 1891, and is named after Fremont, Nebraska, the hometown of two of its founders Luther H. Griffith and Edward Blewett."
    if self.name == 'Lower Queen Anne':
      return "Queen Anne Hill is a neighborhood and geographic feature in Seattle, Washington, northwest of downtown. The neighborhood sits on the highest named hill in the city, with a maximum elevation of 456 feet (139 m). It covers an area of 7.3 square kilometers (2.8 sq mi), and has a population of about 28,000. Queen Anne is bordered by Belltown to the south, Lake Union to the east, the Lake Washington Ship Canal to the north and Magnolia to the west."
    return ""

  @property
  def twitter_widget_id(self):
    if self.name == 'Capitol Hill':
      return "564280607295807489"
    if self.name == 'Wallingford':
      return "564345249208598530"
    if self.name == 'Fremont':
      return "564345130895679489"
    if self.name == 'Lower Queen Anne':
      return "564343097442594818"
    return "0"



################################################################################
# Ad Hoc test
################################################################################

def ad_hoc_test():
  res = Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill')
  pprint(vars(res))
  print res.lat_lng
  print res.zillow_listings_url

if __name__ == '__main__':
  ad_hoc_test()
