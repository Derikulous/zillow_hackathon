from flask import *
import yaml
from yelpapi import YelpAPI
from flickrapi import FlickrAPI
import geocoder
from dataset import Neighborhood
from venues import *
import string
from pprint import pprint

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
    photos = list(flickr_api.walk(privacy_filter=1, lat=47.683937, lon=-122.27431, radius=5, per_page=5))
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
    use_default = True
    enable_recommender = False

    if request.method == 'POST':
      geo_res = try_get_neighborhood_city(request.form['current_address'])
      source_neighborhood = geo_res[0]
      source_city = geo_res[1]

      enable_recommender = bool(request.form.get('algo', False))

      target_city = request.form['future_city'].strip()
      if len(target_city) > 0:
        geo_res = try_get_neighborhood_city(target_city)
        if not geo_res is None:
          target_city = geo_res[1]
          if target_city == 'SF':
            target_city = 'San Francisco'

      if target_city is None:
        target_city = 'Seattle'

      if enable_recommender and not source_neighborhood is None:
        print "Recommendations for moving from %s, %s to %s ..." % (source_neighborhood, source_city, target_city)

        recommender = Recommender.load()

        result = recommender.recommend(source_city, source_neighborhood, target_city)
        recommendations = [ (r, score) for r, score in result ]
        print "Found %d recommendations" % len(recommendations)

        if len(recommendations) > 0:
          use_default = False

    if use_default:
      # For the demo
      recommendations = [
        (Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill'), 0.84),
        (Neighborhood.get_for_city_and_neighborhood('Seattle', 'Fremont'), 0.82),
        (Neighborhood.get_for_city_and_neighborhood('Seattle', 'Wallingford'), 0.78),
        (Neighborhood.get_for_city_and_neighborhood('Seattle', 'Lower Queen Anne'), 0.72)
      ]

    if enable_recommender:
      return render_template('results_dyn.html', recommendations=recommendations)
    else:
      return render_template('results_dyn.html', recommendations=recommendations)

@app.route("/explore/<city>/<neighborhood>")
def explore(city, neighborhood):
    ds = Neighborhood.get_for_city_and_neighborhood(city, neighborhood)

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

    # Hardcode for demo, otherwise get from flickr
    if ds.name == 'Capitol Hill':
      photos = [
        "/static/caphill/broadway31-900x500-fixed.jpg",
        "/static/caphill/blockparty.jpg",
        "/static/caphill/caphill2_900x500-fixed.jpg"
      ]
    if ds.name == 'Wallingford':
      photos = []
    if ds.name == 'Fremont':
      photos = []
    if ds.name == 'Lower Queen Anne':
      photos = []

    hashtag = ''.join(string.capwords(neighborhood.lower()).split(' '))
    return render_template('explore.html', nb=ds, venues=venues, photos=photos, twitter_hashtag=hashtag)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
