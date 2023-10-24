import datetime
import jwt
import os
from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

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
server.route("/login", methods = ["POST"])


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


@server.route("/validate", method = ["POST"])
def validate():
    # Not going to check the type of the authentication scheme here
    # Just going to assume it's of Bearer type - but in production check
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401
    # Authorization: Bearer <token>
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
                encoded_jwt,
                os.environ.get("JWT_SECRET"),
                algorithm = [os.getenv("SERVER_ENCRYPTION_ALGORITHM")]
                )
    except:
        return "not authorized", 403

    return decoded, 200


def create_jwt(username, secret, authorization):
    """
    Create a JSON Web Token (JWT) for the given username, secret, and authorization.

    Args:
        username (str): The username to include in the JWT.
        secret (str): The secret key used to sign the JWT.
        authorization (bool): Whether the user has admin authorization.

    Returns:
        str: The encoded JWT.
    """
    return jwt.encode(
            {
                "username": username,
                "expiration": datetime.datetime.utcnow() + datetime.timedelta(
                        days = int(os.getenv("SERVER_JWT_EXPIRATION"))
                        ),
                "iat": datetime.datetime.utcnow(),
                "admin": authorization,
                },
            secret,
            algorithm = os.getenv("SERVER_ENCRYPTION_ALGORITHM"),
            )


if __name__ == "__main__":
    # If we want to host our server locally but make it accessible
    # we have to set the host to 0.0.0.0 which tells the OS to listen on all public IPs
    # otherwise it will only be accessible from our own computer.
    # We are telling our flask app to listen on all
    # our docker container's IPs for incoming requests.
    server.run(host = "0.0.0.0", port = 5000)
