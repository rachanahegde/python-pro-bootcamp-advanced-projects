from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")

#  When someone makes a GET request to the /random route,
#  the Flask server fetches a random cafe from the database.
# Note: GET is allowed by default on all routes so no need to explicitly include it
@app.route("/random")
def get_random_cafe():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)
    # Server is an API so it should return a JSON containing the relevant data
    # Turn the random_cafe SQLAlchemy Object into a JSON through serialization.
    # Use Flask's serialisation helper method called jsonify() and provide the structure of the JSON to return.
    return jsonify(cafe={
        # Omit the id from the response
        # "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,

        # Put some properties in a sub-category
        "amenities": {
            "seats": random_cafe.seats,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "has_sockets": random_cafe.has_sockets,
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
        }
    })

    # Other method of serialising  the database row Object to JSON is first converting it to a dictionary
    # then using jsonify() to convert the dictionary (which is  similar in structure to JSON) to a JSON.

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
