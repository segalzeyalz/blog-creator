from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["blog-app"]
posts = db["posts"]
users = db["users"]