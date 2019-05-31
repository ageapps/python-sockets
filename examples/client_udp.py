import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from client import Client
from protocol import FragmentProtocol

HOST = "localhost"
PORT = 12344
QUEUE_SIZE = 5
UDP_CLIENT = True
HEADER_SIZE = 20

proto = FragmentProtocol()
socket_adapter = Client(PORT, host=HOST, udp=UDP_CLIENT, protocol=proto)
socket_adapter.send_message("Hello server")

print(socket_adapter.receive_message())

while True:
    time.sleep(2)
    socket_adapter.send_message({ "name": "Time", "time": time.time()})
