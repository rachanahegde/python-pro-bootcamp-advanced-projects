from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
import requests

TMDB_API_KEY = ""

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

# Form for editing movie rating and review
class RateMovieForm(FlaskForm):
    rating = StringField('Your Rating Out of 10')
    review = StringField('Your Review')
    submit = SubmitField('Done')

# Form for adding new movie
class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# Display movies on the home page based on ranking which is determined by rating
@app.route("/")
def home():
    return render_template("index.html", movies=Movies.query.all())

# Edit movie rating and review
@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    movie_id = request.args.get("id")
    movie_to_edit = Movies.query.get(movie_id)
    rate_movie_form = RateMovieForm(id=movie_id)
    if rate_movie_form.validate_on_submit():
        movie_to_edit.rating = float(rate_movie_form.rating.data)
        movie_to_edit.review = rate_movie_form.review.data
        db.session.commit()
        return(redirect(url_for("home")))
    return render_template("edit.html", movie=movie_to_edit, form=rate_movie_form)

# Delete movie from the database
@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

# Add movie to the website
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        title = add_movie_form.title.data
        response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + TMDB_API_KEY + '&query=' + title)
        data = response.json()["results"]
        return render_template("select.html", movies=data)
    return render_template("add.html", form=add_movie_form)  

# Select movie, get data from TMDB API, and add movie to database
@app.route("/find", methods=["GET", "POST"])
def find_movie():
    movie_id = request.args.get("id")
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}")
    data = response.json()
    new_movie = Movies(
        title=data["title"],
        year=data["release_date"].split("-")[0],
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/original/{data['poster_path']}",
    )
    db.session.add(new_movie)
    db.session.commit()
    # Find the movie record in the Movies database 
    movie_record = Movies.query.filter_by(title=data["title"]).first()
    return redirect(url_for("edit_movie", id=movie_record.id))

if __name__ == '__main__':
    app.run(debug=True)
