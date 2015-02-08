import os
from pprint import pprint

from scrapy.selector import Selector

from zillow_hackathon.data.parsers import xfirst, to_float

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

################################################################################
# Neighborhood data
################################################################################

class Neighborhood:
  @staticmethod
  def get_for_city_and_neighborhood(city, neighborhood):
    for n in Neighborhood.get_neighborhoods_in_city(city):
      if n.key == neighborhood.lower().strip():
        return n

    raise KeyError("Did not find neighborhood: %s" % neighborhood)

  @staticmethod
  def get_neighborhoods_in_city(city):
    if city == 'Seattle':
      fname = os.path.join(SCRIPT_DIR, 'data/output/sea_nbr_zillow_raw.tsv')
    elif city == 'San Francisco':
      fname = os.path.join(SCRIPT_DIR, 'data/output/sf_nbr_zillow_raw.tsv')
    else:
      raise ValueError("city should be Seattle or San Francisco")

    with open(fname) as f:
      data = f.readlines()
      for entry in data:
        parts = entry.split('\t')

        xml = parts[1]
        yield Neighborhood(xml)

  def __init__(self, xml_s):
    self.sel = Selector(text = xml_s)

  @property
  def key(self):
    return self.name.lower()

  @property
  def name(self):
    return xfirst(self.sel, '//response/region/neighborhood/text()')

  @property
  def lat_lng(self):
    lat = xfirst(self.sel, '//response/region/latitude/text()')
    lng = xfirst(self.sel, '//response/region/longitude/text()')
    return [float(lat), float(lng)]

  @property
  def median_income(self):
    return to_float(xfirst(self.sel, '//*[name="Median Household Income"]//neighborhood//text()'))

  @property
  def median_age(self):
    return to_float(xfirst(self.sel, '//*[name="Median Age"]//neighborhood//text()'))

################################################################################
# Ad Hoc test
################################################################################

def ad_hoc_test():
  res = Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill')
  print res.name
  print res.lat_lng
  print res.median_income
  print res.median_age

if __name__ == '__main__':
  ad_hoc_test()
