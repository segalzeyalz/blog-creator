# Blog creator
This project enable you to create blogs, posts , like other blog posts

## How to run it?
docker build -t dcoya .
docker run -p 5000:5000 -t -i dcoya

## Rules and checks I added
1. required fields are inside (user, post)
2. user 

## Why mongodb
1. easier to implement - getting the likes and the posts by user very easily, inside the same document
2. Easy for searching

## Tradeoffs made - things we should add
1. Separation of routes
2. Work with a real WSGI
3. Dockerize

## Routes:
### /login, method: Post
login the app, please use an email and password
### /register', method: POST
register the app, please use an email and password
### /posts/<post_id> method: PUT
update metadata about the post - like or dislike
### /posts/<post_id> method: PATCH
Update text and title of a post. please login before
### /posts method: GET
Get all posts
### /posts/ method: POST
Create a post. post should have: title and a text. To do it you should login
### /posts/<post_id> method: DELETE
Delete a post. To do it you should login.
