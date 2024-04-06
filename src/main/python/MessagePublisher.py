import base64
import datetime
import json
import time
from math import floor

import pika
from pika.spec import BasicProperties

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
        self.headers = {}

    def __repr__(self):
        return "Message()"

    def __str__(self):
        return "timestamp={}\nbinary={} bytes".format(self.timestamp, len(self.binary))


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
        props = BasicProperties(
            headers=msg.headers
        )
        self.channel.basic_publish(
            exchange=images_exchange,
            routing_key=images_key,
            properties=props,
            body=json.dumps(
                msg,
                ensure_ascii=True,
                indent=2,
                default=jsonDefaults)
        )

    def publishFrame(self, binary, headers=None):
        msg = Message()
        msg.timestamp = time.time()
        msg.str_datetime = datetime.datetime.fromtimestamp(msg.timestamp)
        msg.headers = headers
        msg.headers['timestamp'] = str(int(msg.timestamp))
        msg.binary = binary
        self.publishMessage(msg)
