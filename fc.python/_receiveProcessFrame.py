import argparse
import base64
import json
import logging.config
import os
import sys
import time

from MessagePublisher import RabbitMQClient

parser = argparse.ArgumentParser(
    description='Receives messages from RabbitMQ, decodes frame from each one and '
                'processes them recognizing faces on the frame')
parser.add_argument(
    "--pid",
    type=int,
    default=0,
    help="Process Meta ID (int) to mark data")
parser.add_argument(
    "--fnum",
    type=int,
    default=10,
    help="Frames number (int)")
parser.add_argument(
    "--qname",
    type=str,
    default="q-input-images",
    help="Queue name (str)")
args = parser.parse_args()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

cnt = 0

def main():
    client = RabbitMQClient()

    def processMessage(ch, method, properties, body):
        try:
            headers = properties.headers
            ts = headers['timestamp']
            frameNo = headers['frameNo']
            logger.info("Processing %s : %s", ts, frameNo)

            jsonMsg = json.loads(body)
            msgBinaryBase64 = jsonMsg['binary']
            msgBinaryDecoded = base64.b64decode(msgBinaryBase64)

            time.sleep(0.500)

            global cnt
            cnt += 1
            cnt %= args.fnum
            filename = "out/file_{}_{}.jpg".format(args.pid, cnt + 1)
            try:
                f = open(filename, "wb")
                f.write(msgBinaryDecoded)
                f.close()
                return 0
            except:
                logger.info("Can't write to file {}".format(filename))
                return 1
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
