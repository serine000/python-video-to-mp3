import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# Creates a Flask web application instance
server = Flask(__name__)

# Creates a MySQL database connection
mysql = MySQL(server)

# Database configurations in our server dictionary
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST") #localhost
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# Creating the routes
server.route('/login', methods = ["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # Check for username and password in database
    cursor = mysql.connection.cursor()
    res = cursor.execute(
            "SELECT email, password FROM user WHERE email=%s",
            (auth.username,)
            )
    # Row found (should be only 1 row)
    if res > 0:
        # result is a tuple
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return create_jwt(auth.username, os.environ.get("JWT_SECRET"), True)

    else:
        # user does not exist
        return "invalid credentials do not exist", 401








