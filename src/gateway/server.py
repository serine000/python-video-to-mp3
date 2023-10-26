import os
import gridfs
import pika
import json

from flask import Flask, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from auth import validate
from auth_service import access
from storage import util

load_dotenv()

server = Flask(__name__)
server.config["MONGO_URI"] = os.getenv("SERVER_ENCRYPTION_MONGODB_URI")

# Manages MongoDB conenction to our flask app
mongo = PyMongo(server)

# Wrap our mongodb to use gridfs
# Handling large files in memory will cause performance degradation, an alternative:
# Gridfs
# GridFS shards the files that are > 16MB
# Instead of storing a file in a single document, GridFS divides the file into chunks
# and stores each chunk as a separate document.
# GridFS uses two collections to store files, one that stores the file chunks and one
# for the file metadata.
fs = gridfs.GridFS(mongo.db)

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("login", methods = ["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    return err

# Validate user before taking their video
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
