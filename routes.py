import datetime
from functools import wraps
from uuid import uuid4
from flask import Flask, jsonify, request, abort, make_response
from factory.adapters.post_adapter import PostAdapter
from factory.adapters.user_adapter import UserAdapter
from factory.validators.post_validator import PostValidator
from factory.validators.user_validator import UserValidator
from werkzeug.security import generate_password_hash
from models import Post, User
from pymongo import MongoClient

from post_extractor import PostExtractor

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["blog-app"]
post_model = Post(PostValidator(), db["posts"], PostAdapter())
user_validator = UserValidator()
user_model = User(user_validator, db["users"], UserAdapter())


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        session_id = headers['sessionId']

        if session_id is None:
            return abort(400)

        user = [item for item in user_model.find({'session.uuid': session_id})][0]
        if not user:
            return abort(400)

        if user['session']['endTime'] < datetime.datetime.now():
            return abort(400)

        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=["POST"])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # actually better practice to seperate this
    current_session_id = request.headers['sessionId']
    if current_session_id:
        user_details = list(user_model.find({"session.uuid": "current_session_id", "email": email}))
        if len(user_details) > 0 and user_details[0]["endTime"] > datetime.datetime.now():
            return user_details[0]["uuid"], 200

    find_user_query = {"email": email, "password": generate_password_hash(password)}
    user = user_model.find(find_user_query)

    if not user:
        return abort(401)
    session = {
        "uuid": uuid4().hex,
        "endTime": datetime.datetime.today() + datetime.timedelta(days=1)
    }
    user_model.update(find_user_query, {"$set": {"session": session}})
    return make_response(session['uuid'], 201)


@app.route('/register', methods=["POST"])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    if user_model.find({"email": email}):
        abort(409)

    is_created, error_msg = user_model.create({"email": email, "password": password})
    if not is_created:
        return abort(415, error_msg)
    return make_response(jsonify("created"), 201)


@app.route("/posts/<post_id>", methods=["PUT"])
@login_required
def like_post(post_id: str):
    try:
        args = request.args
        is_like = args.get('like', None)
        if is_like in ('true', 'false'):
            user = list(user_model.find({'session.uuid': request.headers['sessionId']}))[0]
            email = user["email"]
            blog_post_updated, why_not = post_model.update({'postId': post_id}, {
                "$set": {f"likes.{email}": is_like == 'true'}
            })
            if blog_post_updated:
                return make_response(jsonify("updated"), 204)

            # same functionality for comments

            return blog_post_updated, why_not
        abort(415, "invalid procedure")
    except Exception as e:
        return abort(404)


@app.route("/posts/<post_id>", methods=["PATCH"])
@login_required
def edit_post(post_id: str):
    try:
        user = list(user_model.find({'session.uuid': request.headers['sessionId']}))[0]
        expected_author = user["email"]
        post_model_to_update = list(post_model.find({"author": expected_author, "postId": post_id}))
        if len(post_model_to_update) != 1:
            return jsonify({"message": "This user is not authorised"}), 409

        new_text = request.json.get('text')
        new_title = request.json.get('title')
        update_query = {'$set': {}}
        if new_text:
            update_query['$set']['text'] = new_text
        if new_title:
            update_query['$set']['title'] = new_title
        blog_post_updated, why_not = post_model.update({'postId': post_id}, update_query)
        if blog_post_updated:
            return make_response(jsonify("updated"), 204)
        return abort(401, 'db not updated')
    except Exception as e:
        return abort(404)


@app.route("/posts", methods=["GET"])
@login_required
def get_posts():
    try:
        raw_posts_data = post_model.find({})
        posts = [PostExtractor().extract(post) for post in raw_posts_data]
        return jsonify(posts), 200
    except Exception as e:
        return "not found", 404


@app.route("/posts/", methods=["POST"])
@login_required
def create_post():
    try:
        data = request.get_json()
        text = data["text"]
        title = data["title"]
        post_id = uuid4().hex
        user = list(user_model.find({'session.uuid': request.headers['sessionId']}))[0]
        author = user["email"]
        post_created, error = post_model.create({"postId": post_id, "text": text, "title": title, "author": author})

        if post_created:
            return make_response(f"post {post_id} created", 201)

        return abort(400, f"failed to create the row in db because {error}")
    except Exception as e:
        return abort(400, "failed to create the row in db")


@app.route("/posts/<post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    try:
        user = list(user_model.find({'session.uuid': request.headers['sessionId']}))[0]
        author = user["email"]
        post_deleted, error = post_model.delete({"author": author, "postId": post_id})

        if post_deleted:
            return make_response(f"post {post_id} deleted", 201)

        return abort(400, f"failed to delete as the post is not found or not authorised for this user")
    except Exception as e:
        return abort(400, "failed to create the row in db")
