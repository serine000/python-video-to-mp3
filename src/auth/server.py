import datetime
import jwt
import os
from flask import Flask
from flask import request
from flask_mysqldb import MySQL

# Creates a Flask web application instance
server = Flask(__name__)

# Creates a MySQL database connection
mysql = MySQL(server)

# Database configurations in our server dictionary
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")  # localhost
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# Creating the routes
server.route('/login', methods = ["POST"])


def login():
    """
    Authenticates the user and returns a JWT token if the credentials are valid.

    Returns:
        str: JWT token if the credentials are valid.
        str: Error message if the credentials are invalid or missing.
    """
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    try:
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
            return "user does not exist", 401

    except Exception as e:
        return str(e), 500


def create_jwt(username, secret, authorization):
    return jwt.encode(
            {
                "username": username,
                "expiration": datetime.datetime.now(
                        tz = datetime.timezone.utc
                        ) + datetime.timedelta(days = 1),
                "iat": datetime.datetime.utcnow(),
                "admin": authorization,
                },
            secret,
            algorithm = "HS256",
            )


if __name__ == "__main__":
    # If we want to host our server locally but make it accessible
    # we have to set the host to 0.0.0.0 which tells the OS to listen on all public IPs
    # otherwise it will only be accessible from our own computer.
    # We are telling our flask app to listen on all
    # our docker container's IPs for incoming requests.
    server.run(host = "0.0.0.0", port = 5000)
