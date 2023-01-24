from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["blogs-app"]


@app.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = list(db["blogs"].find())
    return jsonify(blogs)


if __name__ == '__main__':
    app.run(debug=False)
