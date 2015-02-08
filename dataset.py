class Neighborhood:
  @staticmethod
  def get_for_city_and_neighborhood(city, neighborhood):
    if city == 'Seattle':
      fname = 'data/output/sea_nbr_zillow_raw.tsv'
    elif city == 'San Francisco':
      fname = 'data/output/sf_nbr_zillow_raw.tsv'
    else:
      raise ValueError("city should be Seattle or San Francisco")

    with open(fname) as f:
      data = f.readlines()
      for entry in data:
        parts = entry.split('\t')

        if parts[0].lower().strip() == neighborhood.lower().strip():
          xml = parts[1]
          return Neighborhood(xml)

      raise KeyError("Did not find neighborhood " + neighborhood)

  def __init__(self, xmlstring):
    self.xmlstring = xmlstring

  @property
  def lat_lng(self):
    return [47.683937, -122.27431]

  @property
  def median_income(self):
    return int(60819)

  @property
  def median_age(self):
    return int(42)

