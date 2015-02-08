import re

import dateutil.parser

from utils import first

################################################################################
# Regular Expressions
################################################################################

def re_group(text, pattern, default=None):
    if text is None:
        return default

    m = re.search(pattern, text)
    if m:
        return m.group(1).strip()
    else:
        return default

################################################################################
# XPath
################################################################################

def xfirst(sel, xpath, default=None):
    x = sel.xpath(xpath).extract()
    v = first(x, default)

    if v:
        return v.strip()
    else:
        return default

def xtext(xml, xpath):
    return xml.findtext(xpath)

################################################################################
# Number conversion
################################################################################

def to_int(s, val=None):
    if s == None:
        return val

    s = s.replace(',', '')

    try:
        return int(s, 10)
    except ValueError:
        return val

def to_float(s, val=None):
    if s == None:
        return val

    s = s.replace(',', '')
    s = s.lower()

    try:
        mult = 1
        if s.endswith('k'):
            mult = 1000
            s = s[:-1]
        elif s.endswith('m'):
            mult = 1000000
            s = s[:-1]

        return float(s) * mult
    except ValueError:
        return val

################################################################################
# Price
################################################################################

def to_price(s, val=None):
    if s == None:
        return val

    s = s.replace('$', '')
    return to_float(s, val)

################################################################################
# Dates
################################################################################

def to_date(s, default=None):
    if s is None:
        return default

    try:
        return dateutil.parser.parse(s)
    except ValueError:
        return default
