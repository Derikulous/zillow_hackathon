import os
from pprint import pprint

from scrapy.selector import Selector

from data.parsers import xfirst, to_float

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

  @property
  def zillow_listings_url(self):
    return xfirst(self.sel, '//response/links/main/text()')

  @property
  def charts(self):
    names = self.sel.xpath("//response/charts/chart/name/text()").extract()
    urls = self.sel.xpath("//response/charts/chart/url/text()").extract()

    return zip(names, urls)

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
  print res.name
  print res.lat_lng
  print res.median_income
  print res.median_age

if __name__ == '__main__':
  ad_hoc_test()
