from flask import Flask, render_template, request
import requests
import smtplib

MY_EMAIL = ""
MY_PASSWORD = ""

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


@app.route('/post/<int:index>')
def show_post(index):
    return render_template("post.html", index=index, posts=all_posts)


# Contact Form
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Email me the form data submitted by the user
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:New Message\n\n"
                    f"Name: {request.form['name']}\n"
                    f"Email: {request.form['email']}\n"
                    f"Phone: {request.form['phone_number']}\n"
                    f"Message: {request.form['message']}"
            )
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
