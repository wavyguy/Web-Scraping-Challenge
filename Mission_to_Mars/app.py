from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask
app = Flask(__name__)

# Pymongo Connection 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_mars")


# Route 
@app.route("/")

def home():

    # Find Record from Mongo Database 
    destination_data = mongo.db.collection.find_one()

    # Return Template 
    return render_template("index.html", mission=destination_data)


# Route to Scrape 
@app.route("/scrape")

def scrape():

    # Run Scrape 
    mars_data = scrape_mars.scrape_info()
 
    # Update the Mongo Database
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
