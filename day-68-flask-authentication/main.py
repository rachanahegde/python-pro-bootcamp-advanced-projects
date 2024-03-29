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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(1000))

# Line below only required once, when creating DB
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Secure password by hashing and salting it before storage
        hash_and_salted_password = generate_password_hash(
            request.form['password'],
            method='pbkdf2:sha256',
            salt_length=8)
        # Check if user has  registered with this email
        if User.query.filter_by(email=request.form['email']).first() is None:
            # Create a new User object with email, name and password using the form data
            new_user = User(
                email=request.form.get('email'),
                name=request.form.get('name'),
                password=hash_and_salted_password,
            )
            # Save User object into the users.db to register new user
            db.session.add(new_user)
            db.session.commit()
            # Log in and authenticate user after adding details to database
            login_user(new_user)
            return redirect(url_for("secrets"))
        else:
            # Redirect to login page and flash message to tell user they have already registered
            error = "You've already signed up with that email, log in instead!"
            return render_template('login.html', error=error)
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # Query User model to check if a user exists with the email provided
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None:
            # Update error message for user
            error = 'This email does not exist, please try again'
        else:
            # Check stored password hash against entered password hashed
            if check_password_hash(pwhash=user.password, password=request.form['password']):
                # Login and validate the user
                login_user(user)
                # Redirect user to secrets.html
                return redirect(url_for("secrets"))
            else:
                error = 'Password incorrect, please try again.'
    return render_template("login.html", error=error)


# Views that require the user to be logged in can be decorated with @login_required
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    # User downloads the cheat_sheet.pdf file
    return send_from_directory(directory='static', filename='files/cheat_sheet.pdf')



if __name__ == "__main__":
    app.run(debug=True)
