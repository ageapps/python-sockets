import socket
import time
import sys

from helpers import *

HOST = "localhost"
PORT = 12344
QUEUE_SIZE = 5
TCP_CLIENT = False


def send_message(socket, msg_b, destination, tcp=True):
    if tcp:
        socket.sendall(msg_b)
    else:
        socket.sendto(msg_b, destination)

socket_kind = socket.SOCK_STREAM if TCP_CLIENT else socket.SOCK_DGRAM 
try:
    s = socket.socket(socket.AF_INET, socket_kind)
    if TCP_CLIENT:
        s.connect((HOST, PORT))
except socket.error as err:
    print('Failed to start socket | Error: {}'.format(err))
    sys.exit()


msg_b,header_b = get_message_bytes("Hello server")
send_message(s, header_b, (HOST,PORT), tcp=TCP_CLIENT)
send_message(s, msg_b, (HOST,PORT), tcp=TCP_CLIENT)

while True:
    time.sleep(2)
    msg_b, header_b = get_message_bytes("The time is {}".format(time.time()))
    send_message(s, header_b, (HOST,PORT), tcp=TCP_CLIENT)
    send_message(s, msg_b, (HOST,PORT), tcp=TCP_CLIENT)
