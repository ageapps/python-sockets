import socket
import time
import sys

from helpers import *

HOST = "localhost"
PORT = 12344
QUEUE_SIZE = 5


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except socket.error as err:
    print('Failed to start socket | Error: {}'.format(err))
    sys.exit()


msg_b,header_b = get_message_bytes("Hello server")
s.sendall(header_b)
s.sendall(msg_b)

while True:
    time.sleep(2)
    msg_b, header_b = get_message_bytes("The time is {}".format(time.time()))
    s.sendall(header_b)
    s.sendall(msg_b)
