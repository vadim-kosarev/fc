#!/usr/bin/env python
import pika, sys, os

from MessagePublisher import RabbitMQClient

cnt = 0

def main():
    client = RabbitMQClient()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        global cnt
        cnt += 1
        cnt %= 10
        f = open("out/file_{}.txt".format(cnt), "wb")
        f.write(body)
        f.close()


    client.channel.basic_consume(
        queue="q-input-images",
        on_message_callback=callback,
        auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    client.channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
