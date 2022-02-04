import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ------------- Creating an SQLite Database  ---------- #

# Create a connection to a new database (if the database does not exist then it will be created).
# db = sqlite3.connect("books-collection.db")
# Create a cursor to modify the SQLite database
# cursor = db.cursor()

# Create a table in our database
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, rating FLOAT NOT NULL)")

# Create a new entry in the books table and commit the changes to the database
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

# ---------------- Using SQLAlchemy ---------------- #

# Create an SQLite database called new-books-collection.db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a table called books with 4 fields: id, title, author and rating


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


# Create a new record in the books table
new_book = Book(id=1, title='Harry Potter', author='J.K. Rowling', rating=9.3)
db.session.add(new_book)
db.session.commit()

