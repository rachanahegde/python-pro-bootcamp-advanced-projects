from flask import Flask, render_template
import requests

# Getting blog data from JSON bin
response = requests.get("https://api.npoint.io/85695988d19b80684552")
all_posts = response.json()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:index>')
def show_post(index):
    return render_template("post.html", index=index, posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
