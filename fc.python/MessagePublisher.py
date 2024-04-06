import argparse
import base64
import configparser
import json
import logging.config
import math
import random
import socket
import time

import pika
from pika.spec import BasicProperties

# ------------------------------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read("app-config.ini")
SECT_SUFFIX = config.get("DEFAULT", "section_suffix", fallback="")

SECT_BROKER = "broker" + SECT_SUFFIX
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_HOST = "host"
KEY_PORT = "port"
KEY_VHOST = "vhost"
KEY_IMAGES_EXCHANGE = "images_exchange"
KEY_IMAGES_ROUTING_KEY = "images_routing_key"
KEY_MESSAGE_BROKER_NAME = "message_broker_name"
KEY_MESSAGE_BROKER_CLASS = "message_broker_class"

# ------------------------------------------------------------------------------------------------
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Initialized")

# ------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='Publish image message')
parser.add_argument(
    "-f",
    "--file",
    type=str,
    default="../data/dflt_image.jpg",
    help="Source file")
args = parser.parse_args()


# ======================================================================================================================
class MessageFile:
    _binary = None
    _binaryStr = None

    def _calculateBinaryStr(self):
        self._binaryStr = base64.b64encode(self._binary).decode("utf-8")

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, mime, binary, **kwargs):
        self.mime = mime
        self.setBinary(binary)

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "Mime: {}, Lenght: {} bytes".format(self.mime, len(self._binary))

    # ------------------------------------------------------------------------------------------------------------------
    def setBinary(self, binary):
        self._binary = binary
        self._calculateBinaryStr()

    # ------------------------------------------------------------------------------------------------------------------
    def getBinraryStr(self):
        return self._binaryStr

    # ------------------------------------------------------------------------------------------------------------------
    def getBinary(self):
        return self._binary


# ======================================================================================================================
class Message:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, headers, file, **kwargs):
        self.headers = headers
        self.file = file

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "\nHeaders= {}\nfile= {}".format(self.headers, self.file)

    # ----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def jsonSerialize(obj, **kwargs):
        if isinstance(obj, Message):
            return {
                "file": obj.file
            }
        if isinstance(obj, MessageFile):
            return {
                "mime": obj.mime,
                "data": obj.getBinraryStr()
            }
        return None


# ======================================================================================================================
class MQClient:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.description = config.get(SECT_BROKER, KEY_MESSAGE_BROKER_NAME)
        logger.info("Created: %s", self.description)

    # ------------------------------------------------------------------------------------------------------------------
    def publishMessage(self, msg):
        return


# ======================================================================================================================
class RabbitMQClient(MQClient):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._credentials = pika.credentials.PlainCredentials(
            username=config.get(SECT_BROKER, KEY_USERNAME),
            password=config.get(SECT_BROKER, KEY_PASSWORD))
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.get(SECT_BROKER, KEY_HOST),
                port=config.get(SECT_BROKER, KEY_PORT),
                virtual_host=config.get(SECT_BROKER, KEY_VHOST),
                credentials=self._credentials
            ))
        self._channel = self._connection.channel()
        return

    # ------------------------------------------------------------------------------------------------------------------
    def publishMessage(self, message):
        props = BasicProperties(
            headers=message.headers
        )
        sBody = json.dumps(
            message,
            ensure_ascii=True,
            indent=2,
            default=Message.jsonSerialize)
        self._channel.basic_publish(
            exchange=config.get(SECT_BROKER, KEY_IMAGES_EXCHANGE),
            routing_key=config.get(SECT_BROKER, KEY_IMAGES_ROUTING_KEY),
            properties=props,
            body=sBody
        )


# ======================================================================================================================
class KafkaClient(MQClient):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Created")

    # ------------------------------------------------------------------------------------------------------------------
    def publishMessage(self, msg):
        logger.info("publishMessage")
        super().publishMessage(msg)


# ======================================================================================================================
if "__main__" == __name__:
    logger.info("__main__ started")

    mqBroker = globals()[config.get(SECT_BROKER, KEY_MESSAGE_BROKER_CLASS)]()  # !!! -----------------------------------

    logger.info("Created: %s", mqBroker)
    logger.info("Publishing %s", args.file)

    fs = open(args.file, 'rb')
    byteArray = fs.read()
    fs.close()
    msgFile = MessageFile(mime="image/jpg", binary=byteArray)  # !!! ---------------------------------------------------

    logger.info("Publishing %s of %d bytes", msgFile.mime, len(msgFile.getBinary()))

    now = time.time()
    msgHeaders = {
        "hostname": socket.gethostname(),
        "source": args.file,
        "frameNo": random.randint(0, 1000),
        "localID": random.randint(100000, 999999),
        "timestamp": math.floor(now - random.randint(0, 60000)),
        "brokerTimestamp": math.floor(now)
    }

    msg = Message(headers=msgHeaders, file=msgFile)  # !!! -------------------------------------------------------------
    logger.info("msg: %s", msg)

    mqBroker.publishMessage(msg)  # !!! --------------------------------------------------------------------------------
