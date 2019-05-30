import socket
import time
import sys
from server import UDPServer
from protocol import FragmentProtocol

PORT = 12344
HOST = ""
UDP_SERVER = True
HEADER_SIZE = 20

proto = FragmentProtocol()

server = UDPServer(PORT, protocol=proto)
server.start()

while True:
    msg, client_address = server.receive_message()
    print("New message: {} | Sender: {}:{}".format(msg, client_address[0], client_address[1]))
    if isinstance(msg['data'], str):
        welcome_msg = "Welcome to the server"
        print("Sending: {} to {}:{}".format(welcome_msg, client_address[0], client_address[1]))
        server.send_message(welcome_msg, client_address)

server.stop()
