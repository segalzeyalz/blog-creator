from http.client import BAD_REQUEST
import uuid
from flask import jsonify, make_response, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from factory.adapters.post_adapter import PostAdapter
from factory.validators.post_validator import PostValidator

from models.post import PostModel
from db import posts
from post_extractor import PostExtractor

post_model = PostModel(PostValidator(), posts, PostAdapter())


blp = Blueprint("posts", __name__, description="get, update, like and delete posts")


@blp.route('/posts')
class Posts(MethodView):
    def get(self):
        try:
            raw_posts_data = post_model.find({})
            posts = [PostExtractor().extract(post) for post in raw_posts_data]
            return jsonify(posts), 200
        except Exception as e:
         return "not found", 404

    def post(self):
        try:
            data = request.get_json()
            text = data["text"]
            title = data["title"]
            post_id = uuid.uuid4().hex
            post_created, error = post_model.create({
                "postId": post_id,
                "text": text,
                "title": title
            })

            if post_created:
                return make_response(f"post {post_id} created", 201)

            return abort(400, f"failed to create the row in db because {error}")

        except BAD_REQUEST as e:
            abort(code=e.code, name=e.name, description=e.description)
        
        except KeyError as e:
           abort(400, message="Required paramters not included in the request")

        except Exception as e:
         return abort(400, "failed to create the row in db")

@blp.route('/posts/<string:post_id>')
class Post(MethodView):
   def delete(self, post_id: str):
    try:
        post_deleted, error = post_model.delete({"author": "eyal", "postId": post_id})

        if post_deleted:
            return make_response(f"post {post_id} deleted", 201)

        return abort(400, f"failed to delete as the post is not found or not authorised for this user")
    except Exception as e:
        return abort(400, "failed to create the row in db")

   def put(self, post_id: str):
        try:
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


   def patch(self, post_id: str):
    try:
        args = request.args
        is_like = args.get('like', None)
        if is_like in ('true', 'false'):
            #todo: get the real email
            email = 'segaleseo@gmail.com'.replace('.', '[DOT]')
            blog_post_updated, why_not = post_model.update({'postId': post_id}, {
                f"likes.{email}": is_like == 'true'
            })
            if blog_post_updated:
                return make_response(jsonify("updated"), 204)

            return blog_post_updated, why_not

        abort(415, message="invalid procedure")
    except Exception as e:
        return abort(404)