import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# Creates a Flask web application instance
server = Flask(__name__)

# Creates a MySQL database connection
mysql = MySQL(server)

# Database configurations in our server dictionary
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
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





