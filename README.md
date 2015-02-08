# Zillow Hackathon: HopCity

**HopCity** has developed a neighborhood matchmaking technology that uses machine learning from dynamic, publicly available data to better match people to a new neighborhood before they move.  To help over 40 million people moving every year,  HopCity asks the user's current location to recommend neighborhoods in the city they would like to move. The matching algorithm shows the top neighborhoods based on various characteristics analyzed from thousands of data points, and can be further refined via filters interesting to the user, e.g. age, income, attractions, restaurants, nightlife, safety, etc.

![landing](http://i.imgur.com/88aniHk.jpg "Landing page")

![results](http://imgur.com/kqyCIqz "Results page")

![neighborhood](http://imgur.com/fsfGB7b "Neighborhood page")

![yelp](http://imgur.com/LR85yK2 "Yelp recommendations")

The application was created on February 6-8th, 2015. You can view it live [here](http://107.170.241.95/ "HopCity").

## Challenge and Approach

Our submission is for *Challenge #3: helping first-time homebuyers*. How do I find a home that meets my needs, within my budget, in an area that fits my priorities?

Our approach for solving this problem for 8 million people per year who move interstate and almost 40 million people who move between cities was to:
  1. alleviate the fear of moving to a new city by matching them with lifestyle & community neighborhood insights in a unique and easily visual way.
  2. crunch Zillow affordability data API and match homebuyers with neighborhoods that are affordable and a close match to their price point.
  3. use Freebase Knowledge Graph to pull structural entity data about neighbourhoods.
  4. target millenials - the largest first-home buyer generation in the next 10 years by using the Yelp API to show more visual images and descriptions.
  5. match the user, once they settle on a neighborhood, with a set of housing options (Homebuyers then can go to Zillow listings in this area)

## Team Members

+ Andrey Nokhrin @fliptrealestate
+ Evgeny Podlepaev www.linkedin.com/in/podlepaev/en
+ Sam Rexford @samrexford
+ Chris Li www.linkedin.com/in/chrili/en
+ Derik Strattan www.derikstrattan.com

## Technologies, APIs, and Datasets Utilized

We made use of:
  1. *Zillow* affordability data API to match homebuyers with neighborhoods
  2. *Flikr API* to display neighborhood images that are dynamic, like the nature of these communities!
  3. *Yelp API* to display cafes, restaurants, nightclubs, gyms, parks, theaters and markets - all the attributes important to selecting a neighborhood. We show the top results for each category
  4. Google Images API to pull in images for each neighborhood on the results page
  5. IPython Notebook contains some code for data clustering and dimensionality reduction

## Contributing

In order to build & run our app:

	sudo easy_install pip virtualenv
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

Our code is licensed under the [MIT License](license.md). Pull requests will be accepted to this repo, pending review and approval.
