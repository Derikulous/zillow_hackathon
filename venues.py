class VenueType:
  def __init__(self, name, yelp_results):
    self.name = name
    self.yelp_results = yelp_results

  @property
  def results(self):
    return self.yelp_results

class Venue:
  def __init__(self, api_obj):
    self.source = api_job

