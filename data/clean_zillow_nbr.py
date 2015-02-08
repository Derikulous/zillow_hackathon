import os
import json

from scrapy.selector import Selector

from zillow_hackathon.data.parsers import xfirst, to_float

from pprint import pprint

IN_FILES = [
  './output/sea_nbr_zillow_raw.tsv',
  './output/sf_nbr_zillow_raw.tsv'
]

def parse_neighborhood(xml):
  sel = Selector(text = xml)

  parsed = dict()

  parsed['name'] = xfirst(sel, '//response/region/neighborhood/text()')

  parsed['city'] = xfirst(sel, '//response/region/city/text()')
  parsed['state'] = xfirst(sel, '//response/region/state/text()')

  parsed['lat'] = to_float(xfirst(sel, '//response/region/latitude/text()'))
  parsed['lng'] = to_float(xfirst(sel, '//response/region/longitude/text()'))

  parsed['zillow_listings_url'] = xfirst(sel, '//response/links/main/text()')
  parsed['charts_names'] = sel.xpath("//response/charts/chart/name/text()").extract()
  parsed['charts_urls'] = sel.xpath("//response/charts/chart/url/text()").extract()

  num_attrs = parsed['num_attrs'] = dict()
  num_attrs['median_income'] = to_float(xfirst(sel, '//*[name="Median Household Income"]//neighborhood//text()')) or 0
  num_attrs['median_age'] = to_float(xfirst(sel, '//*[name="Median Age"]//neighborhood//text()')) or 0
  num_attrs['median_list_price'] = to_float(xfirst(sel, '//*[name="Median List Price"]//neighborhood//text()')) or 0
  num_attrs['median_value_per_sqft'] = to_float(xfirst(sel, '//*[name="Median Value Per Sq Ft"]//neighborhood//text()')) or 0
  num_attrs['avg_commute_time'] = to_float(xfirst(sel, '//*[name="Average Commute Time (Minutes)"]//neighborhood//text()')) or 0
  num_attrs['pct_with_kids'] = to_float(xfirst(sel, '//*[name="WithKids"]//value//text()')) or 0
  num_attrs['pct_renters'] = to_float(xfirst(sel, '//*[name="Rent"]//value//text()')) or 0
  num_attrs['pct_condo'] = to_float(xfirst(sel, '//*[name="Condo"]//value//text()')) or 0
  num_attrs['pct_built_1900_1919'] = to_float(xfirst(sel, '//*[name="1900-1919"]//value//text()')) or 0
  num_attrs['pct_built_1960_1979'] = to_float(xfirst(sel, '//*[name="1960-1979"]//value//text()')) or 0
  num_attrs['pct_built_1980_1999'] = to_float(xfirst(sel, '//*[name="1980-1999"]//value//text()')) or 0
  num_attrs['pct_built_after_2k'] = to_float(xfirst(sel, '//*[name=">2000"]//value//text()')) or 0
  num_attrs['avg_year_built'] = to_float(xfirst(sel, '//*[name="Avg. Year Built"]//value//text()')) or 0
  num_attrs['pct_single_males'] = to_float(xfirst(sel, '//*[name="Single Males"]//value//text()')) or 0
  num_attrs['pct_single_females'] = to_float(xfirst(sel, '//*[name="Single Females"]//value//text()')) or 0
  num_attrs['avg_household_size'] = to_float(xfirst(sel, '//*[name="Average Household Size"]//value//text()')) or 0
  num_attrs['pct_20s_age'] = to_float(xfirst(sel, '//*[name="20s"]//value//text()')) or 0
  num_attrs['pct_30s_age'] = to_float(xfirst(sel, '//*[name="30s"]//value//text()')) or 0
  num_attrs['pct_commute_10_20_min'] = to_float(xfirst(sel, '//*[name="10-20min"]//value//text()')) or 0
  num_attrs['pct_commute_30_45_min'] = to_float(xfirst(sel, '//*[name="30-45min"]//value//text()')) or 0

  if num_attrs['median_income'] is 0:
    return None

  spec_attrs = parsed['spec_attrs'] = dict()
  for t in sel.xpath('//segmentation/liveshere/title/text()'):
    spec_attrs[t.extract()] = 1

  for t in sel.xpath('//uniqueness//characteristic/text()'):
    spec_attrs[t.extract()] = 1

  return parsed

def process_files():
  for fn in IN_FILES:
    with open(fn) as f:
      for l in f:
        parts = l.split('\t')
        xml = parts[1]

        obj = parse_neighborhood(xml)
        if not obj is None:
          yield obj

for e in process_files():
  print '%s\t%s\t%s\t%s' % (e['state'], e['city'], e['name'], json.dumps(e))
