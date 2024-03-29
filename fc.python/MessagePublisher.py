import time

import pika
import json
import base64
import datetime

username = "root"
userpass = "Password123!"
host = "localhost"
port = 5672
vhost = "fc"
images_exchange = "x-images-input"
images_key = "image"

def jsonDefaults(obj, **kwargs):
    if isinstance(obj, Message):
        return {
            "timestamp": obj.timestamp,
            "str_datetime": str(datetime.datetime.fromtimestamp(obj.timestamp)),
            "binary": base64.b64encode(obj.binary).decode("utf-8")
        }
    return None

class Message:
    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.str_datetime = ""
        self.binary = bytes([])

    def __repr__(self):
        return "Message()"

    def __str__(self):
        return "timestamp={}\nbinary={}".format(self.timestamp, self.binary)


class RabbitMQClient:
    def __init__(self, **kwargs):
        self.credentials = pika.credentials.PlainCredentials(
            username=username,
            password=userpass)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=5672,
                virtual_host=vhost,
                credentials=self.credentials
            ))
        self.channel = self.connection.channel()
        return

    def publishMessage(self, msg):
        self.channel.basic_publish(
            exchange=images_exchange,
            routing_key=images_key,
            body=json.dumps(
                msg,
                ensure_ascii=True,
                indent=2,
                default=jsonDefaults)
        )

    def publishFrame(self, binary):
        msg = Message()
        msg.timestamp = time.time()
        msg.binary = binary
        self.publishMessage(msg)
