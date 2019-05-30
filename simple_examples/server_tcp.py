import socket
import time
import sys
from helpers import *

PORT = 12344
HOST = ""
QUEUE_SIZE = 5
UDP_SERVER = False
HEADER_SIZE = 20


def start_tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) 
    s.listen(QUEUE_SIZE)
    print("TCP socket listening on {}:{}".format(HOST,PORT))
    return s



try:
    server_socket = start_tcp_server()
except socket.error as err:
    print('Failed to start socket | Error: {}'.format(err))
    sys.exit()

while True:
    print("Waiting for clients...")
    client_socket, address = server_socket.accept()
    print("Connected | Client:{}".format(address))
    while True:
        msg = receive_message(client_socket, HEADER_SIZE, UDP_SERVER)
        if msg:
            print("New message: {}".format(msg))
        else:
            print("Disconnected | Client:{}".format(address))
            client_socket.close()
            break

server_socket.close()
