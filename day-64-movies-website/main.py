from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Create an SQLite database called Movies

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a table called Movies
# with these fields: id, title, year, description, rating, ranking, review, img_url

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    # This will allow each movie object to be identified by its title when printed
    def __repr__(self):
        return f'<Movie {self.title}>'

db.create_all()

# Add new movie to the database
# new_movie = Movies(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


# Display movies on the home page
@app.route("/")
def home():
    return render_template("index.html", movies=Movies.query.all())

# Edit movie
@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    if request.method == "POST":
        movie_id = request.form['id']
        movie_to_update = Movies.query.get(movie_id)
        movie_to_update.rating = request.form['new_rating']
        movie_to_update.review = request.form['review']
        db.session.commit()
        return(redirect(url_for("home")))
    movie_id = request.args.get("id")
    movie_to_edit = Movies.query.get(movie_id)
    return render_template("edit.html", movie=movie_to_edit)



if __name__ == '__main__':
    app.run(debug=True)
