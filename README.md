# Tarea3_PCD
A Users API, using SQLAlchemy, FastAPI and SQLite

# Installation
Make sure you have [UV](https://docs.astral.sh/uv/) installed on your machine. Then, in a terminal, move to an empty directory and run `uv build`. 

# Running the application.
To run the application, run `uv run fastapi dev main.py`. You can then open the docs in the link provided to test out the API's endpoints. 

# The Endpoints

## List Users
This is a `GET` request that lists all the current users in the database. 
## Create User
This is a `POST` request that allows you to add a user to the database. You can give them a username, an email, an age, a list of recommendations and a zip code. There are some limitations:
<li> Usernames and user emails are unique to each specific user. Trying to create a new user with a duplicate value will raise an error.
<li> In Mexico, zip codes are 5 digits long, so any zip code smaller or bigger in length will raise an error.

## Update_User
This is a `PUT` request that allows you to change details of an existing user, selected with their unique `id`. The same limitations apply. 

`'/api/v1/{id}'`

## Delete User
This is a `DELETE` request that erases a user from the database, selected with their unique `id`.

`'/api/v1/{id}'`

