import gridfs
import rabbitmq
import pika
import json


def upload_video_to_database(video_file, gridfs_instance, rabbitmq_channel, access_token):
    """
    - Uploads the file to the mongodb database using GridFS.

    Parameters:
        - file: The video file to be uploaded.
        - gridfs_instance: The Mongo GridFS initialized instance.
        - rabbitmq_channel: The RabbitMQ channel to signal available file for processing.
        - str: access_token: The access authentication string to check if user is admin.
    """
    if video_file is None:
        return "invalid file", 400

    try:
        file_id = gridfs_instance.put(video_file)
    except gridfs.errors.GridFSError as err:
        return "internal server error", 500

    queue_message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": access_token["username"],
        }

    try:
        push_message_to_video_queue(
                rabbitmq_channel, queue_message
                )
    except Exception as err:
        gridfs_instance.delete(file_id)
        return "internal server error", 500

    return "upload successful", 200


def push_message_to_video_queue(
        rabbitmq_channel, queue_message
        ):
    """
    Push message to RabbitMQ video queue after it gets uploaded to the database.
    
    Parameters:
        - rabbitmq_channel: RabbitMQ channel
        - queue_message: Message to insert inside the queue
    """
    rabbitmq_channel.basic_publish(
            exchange = "",
            routing_key = "video",
            body = json.dumps(queue_message),
            properties = pika.BasicProperties(
                    # Ensure the messages is durable until it gets removes.
                    delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE,
                    ),
            )
