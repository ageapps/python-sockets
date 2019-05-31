import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from client import Client
from protocol import FragmentProtocol
from protocol import code


HOST = "localhost"
PORT = 12344
QUEUE_SIZE = 5
UDP_CLIENT = True
HEADER_SIZE = 20

proto = FragmentProtocol()
socket_adapter = Client(PORT, host=HOST, udp=UDP_CLIENT, protocol=proto)
msg = {
    'data': 'Hello server',
    'key': 'setup'
}

answer = socket_adapter.send_message(msg, wait_answer=True)
if answer['code'] != code.CODE_OK:
    print('Error in response')
    sys.exit()
elif answer['code'] == code.CODE_OK:
    print('successfully joined server')

while True:
    time.sleep(2)
    new_msg = {"key": "time", "data": time.time()}
    answer = socket_adapter.send_message(new_msg, wait_answer=True)
    if answer['code'] != code.CODE_OK:
        print('Error in response')
        sys.exit()
