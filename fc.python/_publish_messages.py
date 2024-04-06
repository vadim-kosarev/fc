import base64
import json

from MessagePublisher import jsonSerialize, RabbitMQClient, Message

# ----------------------------------------------------------------------------------
msg = Message()
print(msg)
msg.binary = "Hello Ворлд!".encode("utf-8")
print(base64.standard_b64encode(msg.binary))
print(json.dumps(
    msg,
    ensure_ascii=True,
    indent=2,
    default=jsonSerialize))
# ----------------------------------------------------------------------------------

publisher = RabbitMQClient()
publisher.publishFrame("Hello Ворлд!".encode("utf-8"))
