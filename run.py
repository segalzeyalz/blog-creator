from flask import Flask, jsonify, request, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["blog-app"]


def take_post(post: dict):
    return {
        "postId": post["postId"],
        "text": post["text"],
        "likesAmount": len(post["likes"])
    }


@app.route("/posts", methods=["GET"])
def get_posts():
    try:
        raw_posts_data = list(db["posts"].find())
        posts = [take_post(post) for post in raw_posts_data]
        return jsonify(posts)
    except Exception as e:
        print(e)
        return "not found", 404


@app.route("/posts", methods=["POST"])
def create_blog():
    data = request.get_json()
    db["likes"].insert_one({"user_id": data["user_id"], "post_id": data["post_id"]})
    return


@app.route("/posts/<post_id>", methods=["PUT"])
def update_post():
    return "aaa", 200


if __name__ == '__main__':
    app.run(debug=False)
