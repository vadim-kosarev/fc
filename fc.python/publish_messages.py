import base64
import datetime
import json
import time

import pika.credentials


class Message:
    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.str_datetime = ""
        self.binary = bytes([])

    def __repr__(self):
        return "Message()"

    def __str__(self):
        return "timestamp={}\nbinary={}".format(self.timestamp, self.binary)

    @staticmethod
    def jsonDefaults(obj):
        if isinstance(obj, Message):
            return {
                "timestamp": obj.timestamp,
                "str_datetime": str(datetime.datetime.fromtimestamp(obj.timestamp)),
                "binary": base64.b64encode(obj.binary).decode("utf-8")
            }
        return None


# ----------------------------------------------------------------------------------
msg = Message()
msg.timestamp = time.time()
msg.binary = "Hello Ворлд!".encode("utf-8")
# ----------------------------------------------------------------------------------
print(msg)
print(base64.standard_b64encode(msg.binary))
print(json.dumps(msg, ensure_ascii=True, indent=2, default=Message.jsonDefaults))
# ----------------------------------------------------------------------------------
username = "root"
userpass = "pass"
host = "localhost"
port = 5672
vhost = "fc"
images_exchange = "x-images-input"
images_key = "image"

credentials = pika.credentials.PlainCredentials(
    username=username,
    password=userpass)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=host,
        port=5672,
        virtual_host=vhost,
        credentials=credentials
    ))
channel = connection.channel()

channel.basic_publish(
    exchange=images_exchange,
    routing_key=images_key,
    body=json.dumps(msg, ensure_ascii=True, indent=2, default=Message.jsonDefaults)
)
