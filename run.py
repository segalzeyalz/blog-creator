import random
import string
from uuid import uuid4
from flask import Flask, jsonify, request, abort

from factory.adapters.post_adapter import PostAdapter
from factory.validators.post_validator import PostValidator
from models import post
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["blog-app"]
post_model = post.Post(PostValidator(), db["posts"], PostAdapter())


def make_post(blog_post: dict):
    return {
        "postId": blog_post["postId"],
        "title": blog_post.get("title"),
        "text": blog_post.get("text"),
        "likesAmount": len(blog_post.get("likes", []))
    }


@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        raw_posts_data = list(db["posts"].find())
        posts = [make_post(post) for post in raw_posts_data]
        return jsonify(posts)
    except Exception as e:
        return "not found", 404


@app.route("/posts/", methods=["POST"])
def create_post():
    try:
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(700))
        post_model.create({"postId": uuid4().hex, "text": result_str})
    except Exception as e:
        return abort(400, "failed to create the row in db")


if __name__ == '__main__':
    app.run(debug=False)
