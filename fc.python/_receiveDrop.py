import argparse
import logging.config
import os
import sys
import time

from MessagePublisher import RabbitMQClient

parser = argparse.ArgumentParser(
    description='Receives messages from RabbitMQ and drops em')
parser.add_argument(
    "--qname",
    type=str,
    default="q-input-images",
    help="Queue name (str)")
parser.add_argument(
    "--delay",
    type=float,
    default=0.01,
    help="Delay time (float), sec")
args = parser.parse_args()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
client = RabbitMQClient()

cnt = 0


def main():
    def processMessage(ch, method, properties, body):
        try:
            headers = properties.headers
            ts = headers['timestamp']
            frameNo = headers['frameNo']
            logger.info("Processing %s : %s", ts, frameNo)
            time.sleep(0.01)
            return 0
        except:
            logger.info("Error processing message\n{}".format(body))
            return 2

    while True:
        method_frame, header_frame, body = client.channel.basic_get(
            queue=args.qname, auto_ack=False
        )
        if (method_frame != None):
            err = processMessage(
                client.channel,
                body=body,
                method=method_frame,
                properties=header_frame
            )
            if (err):
                client.channel.basic_nack(delivery_tag=method_frame.delivery_tag)
            else:
                client.channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
