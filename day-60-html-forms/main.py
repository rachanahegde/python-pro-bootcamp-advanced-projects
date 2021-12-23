from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


# Use the Flask Request object to get the username and password entered into the form and display it on the page
@app.route('/login', methods=["POST"])
def receive_data():
    name = request.form['username']
    password = request.form['password']
    return f"<h1>Name: {name}, Password: {password}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
