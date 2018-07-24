# Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Start Flask
app = Flask(__name__)
app.config["Mongo_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from Mongo
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_info,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)