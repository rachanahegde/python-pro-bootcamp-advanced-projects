from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = '7eacf21af72212678a4fa90d1830deced9559d7da526450b114593356af61991'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up LoginManager class to allow application to use Flask-Login
login_manager = LoginManager()
# Configure app object for login
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(1000))

# Line below only required once, when creating DB
# db.create_all()


# Set up variable to store the user's name
name = ""


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Create a new User object with email, name and password using the form data
        new_user = User()
        new_user.email = request.form['email']
        new_user.name = request.form['name']
        # Secure password by hashing and salting it before storage
        hash_and_salted_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        new_user.password = hash_and_salted_password
        # Save User object into the users.db to register new user
        db.session.add(new_user)
        db.session.commit()
        # Update global variable
        global name
        name = new_user.name
        # Redirect user to secrets.html
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User()
        # Login and validate the user
        # user should be an instance of your `User` class
        login_user(user)
        password = request.form['password']
        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # Check the user's password
        if check_password_hash(pwhash=pwhash, password=password):
            # Redirect user to secrets.html
            return redirect(url_for("secrets"))
    return render_template("login.html")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Next - checks to see if the username and password match (against your database)
# If authentication was successful you should pass an instance of the user to login_user()

# Views that require the user to be logged in can be decorated with @login_required
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    # User downloads the cheat_sheet.pdf file
    return send_from_directory(directory='static', filename='files/cheat_sheet.pdf')



if __name__ == "__main__":
    app.run(debug=True)
