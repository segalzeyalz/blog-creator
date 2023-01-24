from flask import Flask, jsonify, request, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["blogs-app"]


@app.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = list(db["blogs"].find())
    return jsonify(blogs)


@app.route("/blogs", methods=["POST"])
def create_blog():
    data = request.get_json()
    db["likes"].insert_one({"user_id": data["user_id"], "post_id": data["post_id"]})


if __name__ == '__main__':
    app.run(debug=False)
