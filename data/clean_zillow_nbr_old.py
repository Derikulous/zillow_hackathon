import os
import sys

from scrapy.selector import Selector
from parsers import xfirst

#
# Unfinished
#
with open('./output/sf_nbr_zillow_raw.tsv') as f:
    for line in f:
        parts = line.split('\t')

        xml = parts[1]
        sel = Selector(text = xml)

        for page in sel.xpath('//pages/page'):
            for table in page.xpath('.//table'):
                tab_name = xfirst(table, './name/text()')

                for attr in table.xpath('.//attribute'):
                    name = xfirst(attr, './name/text()')
                    print '%s: %s' % (tab_name, name)

        break

