import os
import json

from pprint import pprint

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

################################################################################
# Neighborhood data
################################################################################

class Neighborhood:
  @staticmethod
  def get_for_city_and_neighborhood(city, neighborhood):
    for n in Neighborhood.get_neighborhoods_in_city(city):
      if n.name.lower() == neighborhood.lower():
        return n

    raise KeyError("Did not find neighborhood: %s" % neighborhood)

  @staticmethod
  def get_neighborhoods_in_city(city):
    for n in Neighborhood.get_neighborhoods():
      if n.city.lower() == city.lower():
        yield n

  @staticmethod
  def get_neighborhoods():
    with open(os.path.join(SCRIPT_DIR, 'data/output/nbr_zillow_clean.tsv')) as f:
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
  def zillow_listings_url(self):
    return xfirst(self.sel, '//response/links/main/text()')

  @property
  def charts(self):
    names = self.sel.xpath("//response/charts/chart/name/text()").extract()
    urls = self.sel.xpath("//response/charts/chart/url/text()").extract()

    return zip(names, urls)

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
