from flask import *
import yaml
from yelpapi import YelpAPI
from flickrapi import FlickrAPI
import geocoder
from zillow_hackathon.dataset import Neighborhood
from venues import *
import string
from pprint import pprint
import pickle

from recommender import Recommender, NumFeaturizer, SpecFeaturizer, Data

app = Flask(__name__)

try:
    with open('secrets.yaml') as f:
        secrets = yaml.load(f.read())

    yelp_api = YelpAPI(secrets['yelp']['consumer_key'], secrets['yelp']['consumer_secret'], secrets['yelp']['token'], secrets['yelp']['token_secret'])
    flickr_api = FlickrAPI(secrets['flickr']['key'], secrets['flickr']['secret'])
except IOError:
    print "MISSING secrets.yaml: ask chris for this file or you'll have a bad time"

def getYelp(query, location, lat_lng):
    print "Query yelp for", query
    search_results = yelp_api.search_query(term=query, limit=5, sort=2, location=location)
    return search_results['businesses']

def getPhotos(lat, lng):
    photos = list(flickr_api.walk(privacy_filter=1, lat=lat, lon=lng, radius=5, per_page=5))
    return photos

@app.route("/")
def home():
    return render_template('home.html', name='Hello')

def try_get_neighborhood_city(address):
    if address is None:
      return ''

    location = geocoder.google(address)

    if location.ok:
      return (location.neighborhood, location.city)
    else:
      return (None, None)

@app.route("/results", methods=["POST", "GET"])
def results():
    print request.form
    use_default = True
    enable_recommender = True

    try:
      if request.method == 'POST':
        res = try_get_neighborhood_city(request.form['current_address'])
        source_neighborhood = res[0]
        source_city = res[1]

        print "Geocoder found neighborhood", source_neighborhood, "in", source_city

        target_city = request.form['future_city'].strip()
        if len(target_city) == 0:
          target_city = 'Seattle'

        if enable_recommender and not source_neighborhood is None:
          print "Recommendations for moving from %s, %s to %s ..." % (source_neighborhood, source_city, target_city)

          recommender = Recommender.load()

          result = recommender.recommend(source_city, source_neighborhood, target_city)
          recommendations = [ r for r, score in result ]

          if len(recommendations) > 0:
            use_default = False
    except Exception as e:
      print "Exception: ", e

    if use_default:
      # For the demo
      recommendations = [
        Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill'),
        Neighborhood.get_for_city_and_neighborhood('Seattle', 'Fremont'),
        Neighborhood.get_for_city_and_neighborhood('Seattle', 'Wallingford'),
        Neighborhood.get_for_city_and_neighborhood('Seattle', 'Lower Queen Anne')
      ]

    return render_template('results.html', recommendations=recommendations, back=['Change Search', '/'])

def get_yelp_for_neighborhood(ds, city):
  yelp_cache_file = 'data/yelp_cache/' + ds.name + '.pickle'
  try:
    with open(yelp_cache_file) as f:
      venues = pickle.load(f)
  except IOError:
    location_query = ds.name + ', ' + city
    venues = [
      VenueType("Restaurants", getYelp('restaurants', location_query, ds.lat_lng)),
      VenueType("Cafes", getYelp('cafes', location_query, ds.lat_lng)),
      VenueType("Bars", getYelp('bars', location_query, ds.lat_lng)),
      VenueType("Nightclubs", getYelp('nightclubs', location_query, ds.lat_lng)),
      VenueType("Gyms", getYelp('gyms', location_query, ds.lat_lng)),
      VenueType("Parks", getYelp('parks', location_query, ds.lat_lng)),
      VenueType("Theaters", getYelp('theaters', location_query, ds.lat_lng)),
      VenueType("Markets", getYelp('markets', location_query, ds.lat_lng))
    ]

    with open(yelp_cache_file, 'wb') as f:
      pickle.dump(venues, f)

  return venues

@app.route("/explore/<city>/<neighborhood>")
def explore(city, neighborhood):
    ds = Neighborhood.get_for_city_and_neighborhood(city, neighborhood)

    venues = get_yelp_for_neighborhood(ds, city)

    # Hardcode for demo, otherwise get from flickr
    if ds.name == 'Capitol Hill':
      photos = [
        "/static/caphill/broadway31-900x500-fixed.jpg",
        "/static/caphill/blockparty.jpg",
        "/static/caphill/caphill2_900x500-fixed.jpg"
      ]
    if ds.name == 'Wallingford':
      photos = [
        "/static/wallingford/wallingford_carousel.jpg",
        "/static/wallingford/wallingford_carousel_2.jpg",
        "/static/wallingford/wallingford_carousel_3.jpg"
      ]
    if ds.name == 'Fremont':
      photos = [
        "/static/fremont/fremont_carousel.jpg",
        "/static/fremont/fremont_carousel_2.jpg",
        "/static/fremont/fremont_carousel_3.jpg"
      ]
    if ds.name == 'Lower Queen Anne':
      photos = [
        "/static/lowerqueenanne/lower_queen_anne_carousel.jpg",
        "/static/lowerqueenanne/lower_queen_anne_carousel_2.jpg",
        "/static/lowerqueenanne/lower_queen_anne_carousel_3.jpg"
      ]

    import time
    time.sleep(0.5)

    hashtag = ''.join(string.capwords(neighborhood.lower()).split(' '))
    return render_template('explore.html', nb=ds, venues=venues, photos=photos, twitter_hashtag=hashtag, back=['Other Recommendations', '/results'])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
