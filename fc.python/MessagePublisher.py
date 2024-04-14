import configparser
import logging.config
import math
import random
import socket
import time
import uuid

import pika
from pika.spec import BasicProperties

from DataStruct import *
import ArgParser

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

KEY_EXCHANGE_INDEXED_IMAGES = "x_indexed_image"
KEY_EXCHANGE_INDEXED_DATA = "x_indexed_data"

# ------------------------------------------------------------------------------------------------
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Initialized")

# ======================================================================================================================
class MQClient:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.description = config.get(SECT_BROKER, KEY_MESSAGE_BROKER_NAME)
        logger.info("Created: %s", self.description)

    # ------------------------------------------------------------------------------------------------------------------
    def publishMessage(self, exchangeKey, headers, body):
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
    def publishMessage(self, exchangeKey, headers, body):
        props = BasicProperties(
            headers=headers
        )

        self._channel.basic_publish(
            exchange=config.get(SECT_BROKER, exchangeKey),
            routing_key=config.get(SECT_BROKER, KEY_IMAGES_ROUTING_KEY),
            properties=props,
            body=body
        )


# ======================================================================================================================
class KafkaClient(MQClient):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Created")

    # ------------------------------------------------------------------------------------------------------------------
    def publishMessage(self, exchangeKey, headers, body):
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

    logger.info("Publishing %s of %d bytes", msgFile.getMime(), len(msgFile.getBinary()))

    now = time.time()
    msgHeaders = {
        "hostname": socket.gethostname(),
        "source": args.file,
        "frameNo": random.randint(0, 1000),
        "localID": random.randint(100000, 999999),
        "timestamp": math.floor(now - random.randint(0, 60000)),
        "brokerTimestamp": math.floor(now),
        "uuid": str(uuid.uuid4())
    }

    msg = Message(headers=msgHeaders, file=msgFile)  # !!! -------------------------------------------------------------
    logger.info("msg: %s", msg)

    mqBroker.publishMessage(msg)  # !!! --------------------------------------------------------------------------------
