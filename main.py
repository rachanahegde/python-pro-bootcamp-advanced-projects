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

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}

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
    # Convert the random_cafe data record to a dictionary of key-value pairs.
    # return jsonify(cafe=random_cafe.to_dict())


# HTTP GET - All the Cafes
@app.route("/all")
def get_all_cafes():
    cafes = Cafe.query.all()
    # Use list comprehension
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


# HTTP GET - Find a Cafe
@app.route("/search")
def search_cafe():
    loc = request.args.get("loc")
    cafes = Cafe.query.all()
    for cafe in cafes:
        if cafe.location == loc:
            return jsonify(cafe=cafe.to_dict())

    return jsonify(error={
        "Not Found": "Sorry, we don't have a cafe at that location."
    })


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(name=request.form.get("name"),
                    location=request.form.get("loc"),
                    map_url=request.form.get("map_url"),
                    img_url=request.form.get("img_url"),
                    seats=request.form.get("seats"),
                    has_toilet=bool(request.form.get("has_toilet")),
                    has_wifi=bool(request.form.get("has_wifi")),
                    has_sockets=bool(request.form.get("has_sockets")),
                    can_take_calls=bool(request.form.get("can_take_calls")),
                    coffee_price=request.form.get("coffee_price"))
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PATCH - Update Coffee Price for a Cafe Record
@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)
    new_price = request.args.get("new_price")
    try:
        cafe.coffee_price = new_price
    except AttributeError:
        # Pass an HTTP code with your response: #404 = Resource not found
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404
    else:
        db.session.commit()
        # 200 = Ok
        return jsonify(response={"success": "Successfully updated the price."}), 200


# HTTP DELETE - Delete Record for a Closed Cafe


if __name__ == '__main__':
    app.run(debug=True)
