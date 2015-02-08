from flask import *
import yaml
from yelpapi import YelpAPI
from flickrapi import FlickrAPI
import geocoder
from dataset import Neighborhood
from venues import *
import string
from pprint import pprint

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

def try_get_neighborhood(address):
    if address is None:
      return ''

    location = geocoder.google(address)

    if location.ok:
      return location.neighborhood
    else:
      return ''

@app.route("/results", methods=["POST", "GET"])
def results():
    if request.method == 'POST':
      # We're getting data from user
      neighborhood = try_get_neighborhood(request.form['current_address'])
      print neighborhood, request.form['current_address'], request.form['future_city']
      pass
    else:
      pass

    # For the demo
    recommendations = [
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill'),
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Ballard'),
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Fremont')
    ]

    return render_template('results.html', recommendations=recommendations)

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
