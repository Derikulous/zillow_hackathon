from flask import *
import yaml
from yelpapi import YelpAPI
from flickrapi import FlickrAPI
from dataset import Neighborhood
app = Flask(__name__)

try:
    with open('secrets.yaml') as f:
        secrets = yaml.load(f.read())

    yelp_api = YelpAPI(secrets['yelp']['consumer_key'], secrets['yelp']['consumer_secret'], secrets['yelp']['token'], secrets['yelp']['token_secret'])
    flickr_api = FlickrAPI(secrets['flickr']['key'], secrets['flickr']['secret'])
except IOError:
    print "MISSING secrets.yaml: ask chris for this file or you'll have a bad time"

def getYelpRestaraunts(location):
    search_results = yelp_api.search_query(term="food", limit=10, sort=2, radius_filter=5, location=location)
    return search_results

def getPhotos(lat, lng):
    photos = list(flickr_api.walk(privacy_filter=1, lat=47.683937, lon=-122.27431, radius=5, per_page=5))
    return photos

@app.route("/")
def home():
    return render_template('home.html', name='Hello')

@app.route("/results", methods=["POST", "GET"])
def results():
    recommendations = [
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Capitol Hill'),
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Ballard'),
      Neighborhood.get_for_city_and_neighborhood('Seattle', 'Fremont')
    ]

    return render_template('results.html', recommendations=recommendations)

@app.route("/explore/<city>/<neighborhood>")
def explore(city, neighborhood):
    ds = Neighborhood.get_for_city_and_neighborhood(city, neighborhood)
    return render_template('explore.html', nb=ds, photos=[])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
