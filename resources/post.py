import uuid

from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify, make_response, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from http.client import BAD_REQUEST

from factory.adapters.user_adapter import UserAdapter
from factory.validators.user_validator import UserValidator


from factory.adapters.post_adapter import PostAdapter
from factory.validators.post_validator import PostValidator
from factory.validators.user_validator import UserValidator

from models.post import PostModel
from models.user import UserModel

from post_extractor import PostExtractor

from schemas import PostSchema, PostUpdateSchema

from db import posts, users as users_db


post_model = PostModel(PostValidator(), posts, PostAdapter())
user_model = UserModel(UserValidator(), users_db, UserAdapter())


blp = Blueprint("posts", __name__, description="get, update, like and delete posts")

@blp.route('/posts')
class Posts(MethodView):

    @jwt_required()
    @blp.response(200, PostSchema(many=True))
    def get(self):
        try:
            raw_posts_data = post_model.find({})
            posts = [PostExtractor().extract(post) for post in raw_posts_data]
            return jsonify(posts), 200
        except Exception as e:
         return "not found", 404
    
    @jwt_required()
    @blp.arguments(PostSchema)
    @blp.response(201)
    def post(self, post_data):
        jwt_info = get_jwt()
        try:
            text = post_data["text"]
            title = post_data["title"]
            post_id = uuid.uuid4().hex
            user_identifier = jwt_info["sub"]

            users = user_model.find({"email": user_identifier})
            author = users[0]
            post_created, error = post_model.create({
                "postId": post_id,
                "text": text,
                "title": title,
                "author": author["email"]
            })

            if post_created:
                return make_response(f"post {post_id} created", 201)

            return make_response(f"Post not created because {error}", 401)
        except BAD_REQUEST as e:
            abort(code=e.code, name=e.name, description=e.description)
        
        except KeyError as e:
           abort(400)

        except Exception as e:
         return abort(400, "failed to create the row in db")

@blp.route('/posts/<string:post_id>')
class Post(MethodView):

   @jwt_required()
   @blp.response(200)
   def get(self, post_id: str):
      posts = post_model.find({"postId": post_id})
      post = posts[0]
      post = PostExtractor().extract(post)
      return post
   
   @jwt_required()
   @blp.response(201)
   def delete(self, post_id: str):
    try:
        jwt_info = get_jwt()

        post_deleted, error = post_model.delete({"author": jwt_info["sub"], "postId": post_id})

        if post_deleted:
            return make_response(f"post {post_id} deleted", 201)

        return abort(400, f"User not authorised to make this action")
    except Exception as e:
        return abort(400, "failed to create the row in db")

   @jwt_required()
   @blp.arguments(PostUpdateSchema)
   @blp.response(204)
   def put(self, post_id: str, updated_data):
        try:
            jwt_info = get_jwt()
            new_text = updated_data.get('text')
            new_title = updated_data.get('title')
            update_query = {'$set': {}}

            if new_text:
                update_query['$set']['text'] = new_text

            if new_title:
                update_query['$set']['title'] = new_title

            blog_post_updated, why_not = post_model.update({'postId': post_id, "author": jwt_info["sub"]}, update_query)

            if blog_post_updated:
                return make_response(jsonify("updated"), 204)

            return abort(401, why_not)
        except Exception as e:
           return abort(404)
   
   @jwt_required()
   @blp.response(204)
   def patch(self, post_id: str):
    try:
        # Like post
        args = request.args
        is_like = args.get('like', None)

        if is_like in ('true', 'false'):
            jwt_info = get_jwt()
            user_identifier = jwt_info["sub"]

            email = user_identifier.replace('.', '[DOT]')
            blog_post_updated, why_not = post_model.update({'postId': post_id}, {
                f"likes.{email}": is_like == 'true'
            })

            if blog_post_updated:
                return make_response(jsonify("updated"), 204)
        

            return blog_post_updated, why_not

        abort(415, message="invalid procedure")
    except Exception as e:
        abort(404)