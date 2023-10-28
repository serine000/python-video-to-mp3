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

# Manages MongoDB connection to our flask app
mongo = PyMongo(server)

# Wrap our mongodb to use GridFS
# Handling large files in memory will cause performance degradation, an alternative:
# GridFS shards the files that are > 16MB
# Instead of storing a file in a single document, GridFS divides the file into chunks
# and stores each chunk as a separate document.
# GridFS uses two collections to store files, one that stores the file chunks and one
# for the file metadata.
gridfs_instance = gridfs.GridFS(mongo.db)

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods = ["POST"])
def gateway_login():
    """
     Authenticates the user and returns a JWT token
     if the credentials are valid at the gateway.

    Returns:
        str: JWT token if the credentials are valid.
        str: Error message if the credentials are invalid or missing.
    """
    token, err = access.check_login(request)

    if not err:
        return token
    return err


# Validate user before taking their video
@server.route("/upload", methods = ["POST"])
def upload_file():
    """
     Takes 1 video file from the user to then uploads it to the database
     and send in a processing message into the queue.

     Returns:
            str: Success message if the file was successfully uploaded.
            str: Error message if the access token is invalid.
     """
    access, err = validate.check_token(request)

    # deserialize the json web token
    access_token = json.loads(access)

    # if user is authorized
    if access_token["admin"]:
        # Upload one file at a time
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400

        for _, video_file in request.files.items():
            err = util.upload_video_to_database(
                    video_file,
                    gridfs_instance,
                    channel,
                    access_token
                    )

            if err:
                return err
    else:
        return "not authorized", 401

    return "success", 200


@server.route("/download", methods = ["GET"])
def download_mp3():
    """
    Download the MP3 file that was generated from the uploaded video.

    Returns:
        file: The MP3 file stored in the database.
    """
    pass


if __name__ == "__main__":
    server.run(host = "0.0.0.0", port = 8080)
