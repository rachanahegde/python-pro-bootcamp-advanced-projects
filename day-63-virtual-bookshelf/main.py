from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Create an SQLite database called library.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a table called library with 4 fields: id, title, author and rating
class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


@app.route('/')
def home():
    # Read all records
    return render_template('index.html', books=Library.query.all())

# Delete a record from the table
@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_to_delete = Library.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# Create a new record in the library table
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Library(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        # You can use the redirect method from flask to redirect to another route
        # e.g. in this case to the home page after the form has been submitted.
        return redirect(url_for('home'))
    return render_template('add.html')

# Edit a record in the Library table
@app.route('/edit', methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        book_id = request.form['id']
        Library.query.get(book_id).rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    return render_template('edit-rating.html', book_id=book_id, library=Library)


if __name__ == "__main__":
    app.run(debug=True)

