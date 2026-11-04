# packages
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# setting required database and collection
db = client["flask_assignment"]
collection = db["students"]

# API endpoint to return data from data.json
@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)

# Home route to render the index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit():

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        course = request.form.get("course")

        if not name or not email or not course:
            return render_template(
                "index.html",
                error="All fields are required."
            )

        student = {
            "name": name,
            "email": email,
            "course": course
        }

        collection.insert_one(student)

        return redirect(url_for("success"))

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error: {str(e)}"
        )

# Route to render the success.html template
@app.route("/success")
def success():
    return render_template("success.html")

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)