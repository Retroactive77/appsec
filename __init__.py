from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, abort
from firebase_admin import credentials, db
from flask_limiter import Limiter
import re
import firebase_admin
import pyrebase
import random
import requests
import time


app = Flask(__name__)
limiter = Limiter(app)

app.secret_key = "3wEcr_spASP-b20u_rl*"

firebase_config = {
    "apiKey": "AIzaSyBKEiTRqZrYGQuwmreu4bDiUN9gwe9j1Lk",
    "authDomain": "appsec2-8c9a7.firebaseapp.com",
    "databaseURL": "https://appsec2-8c9a7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "appsec2-8c9a7",
    "storageBucket": "appsec2-8c9a7.appspot.com",
    "messagingSenderId": "548391003458",
    "appId": "1:548391003458:web:388e9a31f15c041d3cd4dbf",
    "serviceAccount": "E:/appsec2-8c9a7-firebase-adminsdk-m5vxm-0e6ad1c53d.json"
}

cred = credentials.Certificate("E:/appsec2-8c9a7-firebase-adminsdk-m5vxm-0e6ad1c53d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://appsec2-8c9a7-default-rtdb.asia-southeast1.firebasedatabase.app'
})

firebase = pyrebase.initialize_app(firebase_config)
db1 = firebase.database()

def get_random_data():
    ref = db.reference("blog")
    data = ref.get()
    if data:
        random_key = random.choice(list(data.keys()))
        return data[random_key]
    else:
        return None

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error_message = "Page not found!"), 404

@app.errorhandler(Exception)
def server_error(error):
    return render_template("error.html", error_message = "Internal Server Error, please try again."), 500

@app.route('/')
@limiter.limit("30 per minute")
def index():
    return render_template("index.html")

@app.route('/error-example')
def error_example():
    # Simulate a 404 Not Found error
    return abort(404)

@app.route('/exception-example')
def exception_example():
    # Simulate a server-side exception
    raise Exception("Example exception")

@app.route('/aboutus', methods = ["GET", "POST"])
@limiter.limit("10 per minute")
def aboutus():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        content = request.form["feedback"]

        data = {"name": name, "email": email, "feedback": content}
        db1.child("feedback").push(data)

        message = "Thank you for submitting feedback! We will get back to you within 7 days business days! :)"
    return render_template("aboutus.html", message = message)

@app.route('/blog')
def blog():
    message = get_flashed_messages()
    random_data = get_random_data()
    return render_template("blog2222.html", message = message, random_data = random_data)

@app.route('/bloginsert', methods=["GET", "POST"])
def bloginterface():
    message = None
    if request.method == "POST":
        name = request.form["name33"]
        blog_title = request.form["title33"]
        blog_content = request.form["contents33"]

        name_regex = r"^[a-zA-Z\s]+$"
        title_regex = r"^[a-zA-Z0-9\s'\"\-.,!?]+$"
        content_regex = r"^[\s\S]+$"

        if not re.match(name_regex, name) or not re.match(title_regex, blog_title) or not re.match(content_regex, blog_content):
            message = "Invalid inputs. Please provide valid data."
            return render_template('blogwrite_if.html', message = message)

        data = {"name": name, "blog_title": blog_title, "blog_content": blog_content}
        db1.child("blog").push(data)

        flash("Blog has been uploaded!")
        return redirect(url_for('blog'))
    return render_template("blogwrite_if.html")

@limiter.request_filter
def rate_limit_exceeded():
    return "Too many requests", 429

if __name__ == '__main__':
    app.run()
