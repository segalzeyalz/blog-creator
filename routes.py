import datetime
from functools import wraps
from uuid import uuid4
from flask import Flask, jsonify, request, abort, make_response
from flask_smorest import Api

from werkzeug.security import generate_password_hash
from resources.post import blp as PostBlueprint

app = Flask(__name__)

app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Blog Manager"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.1.3/"

api = Api(app)

api.register_blueprint(PostBlueprint)
