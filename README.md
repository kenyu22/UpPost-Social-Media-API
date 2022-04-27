Social Media API built with FastAPI that allows only authorized users to create posts, delete their own posts, update their own posts, and vote/like a post. Conforms to the REST API architectural style, implemented get, post, put, and delete methods. Implemented JWT Authentication to authenticate users when logging in, as well as password hash to prevent a breach of information in our PostgreSQL database. Tables were created using both raw SQL code as well as SQLAlchemy - connected to the database. Non-authenticated users are still able to get all posts, view specific posts, and get specific users.

Deployed on Heroku:
https://uppost-kenny.herokuapp.com/docs
