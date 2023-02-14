from flask import abort, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import users as users_db
from factory.adapters.user_adapter import UserAdapter
from factory.validators.user_validator import UserValidator
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from blocklist import BLOCKLIST

from passlib.hash import pbkdf2_sha256

from schemas import UserSchema

pbkdf2_sha256.default_rounds = 26000
pbkdf2_sha256.default_salt_size = 16

user_model = UserModel(UserValidator(), users_db, UserAdapter())

blp = Blueprint("Users", __name__, description="get, update and delete userts")

@blp.route('/register')
class UserRegister(MethodView):

    @blp.response(201, UserSchema)
    @blp.arguments(UserSchema, required=True, description="register new user", example={
        "email": "Email@example.com", "password": "somePa$$word132" })
    def post(self, user_data: dict):
        users = user_model.find({"email":user_data["email"]})
        if len(users) != 0:
            return {"error_message": "User already exists"}, 400 

        hashed_password = pbkdf2_sha256.hash(user_data["password"])
        was_created = user_model.create({ "email": user_data["email"], "password": hashed_password })

        if was_created:
            return {"message": "User created successfully."}, 201

        return {"error_message": 'db not updated'}, 400


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        found_users = user_model.find({"email": user_data["email"]})
        if len(found_users) == 0:
            return {"error_message": "User not exists"}, 400 


        user = found_users[0]
        if pbkdf2_sha256.verify(user_data["password"], user["password"]):
            access_token = create_access_token(identity=user["email"], fresh=True)
            refresh_token = create_refresh_token(identity=user["email"])
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
