# Blog creator
This project enable you to create blogs, posts , like other blog posts

## How to run it?
docker build -t dcoya .
docker run -p 5000:5000 -t -i dcoya

## Rules and checks I added
1. required fields are inside each request
2. text and title of each post are checked - if contains any profanity or other inappropriate language
3. author - is email

## Why mongodb
Overall, MongoDB is a good fit for this mini blog site due to its ease of use, powerful querying capabilities, and scalability. It will make it easy to store and retrieve data related to your posts and users, while also allowing you to scale your site as it grows.

1. Easy to manage relationships
2. Simple data structure: This site only has two collections: posts and users
3. Easy to query

Routes: look in the swagger: 
/swagger-ui