# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import mymars
#from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#mongo = PyMongo(app)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Getting News
    news_list = list(db.mars_news.find())
    #Getting Feature Image URL
    feature_url=db.mars_feature_url.find()
    #Getting Mars weather
    weather_detail=db.mars_weather.find()
    #Getting Mars geography
    geo_detail=db.mars_geo.find()
    #Getting Mars Hemisperes
    hem_detail=db.mars_hem.find()

    # return template and data
    return render_template("index.html", news=news_list,furl=feature_url,weather=weather_detail,geo=geo_detail,hem=hem_detail)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    # Run scraped functions
    #Get News
    news = mymars.get_mars_news()
    collection = db.mars_news
    collection.drop()
    collection.insert(news)

    #Get Featured URL
    feature_url=mymars.get_mars_featureImg()
    collection = db.mars_feature_url
    collection.drop()
    collection.insert(feature_url)

    #Get Mars Weather
    weather=mymars.get_mars_weather()
    collection = db.mars_weather
    collection.drop()
    collection.insert(weather)

    #Get Mars Geography
    geo=mymars.get_mars_geo()
    collection = db.mars_geo
    collection.drop()
    collection.insert_many(geo)


    #Get Mars Hemisperes
    Hemisperes=mymars.get_mars_hem()
    collection = db.mars_hem
    collection.drop()
    collection.insert_many(Hemisperes)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
