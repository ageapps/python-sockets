import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from server import UDPRServer
from protocol import FragmentProtocol
from protocol import code

PORT = 12344
HOST = ''
UDP_SERVER = True
HEADER_SIZE = 20

proto = FragmentProtocol()

server = UDPRServer(PORT, protocol=proto)
server.start()

while True:
    msg, client_address = server.receive_message(send_answer=False)
    data = msg['data']
    key = msg['key']
    if key == 'setup':
        print(key + ' | message: {} | sender: {}:{}'.format(data, client_address[0], client_address[1]))
        welcome_msg = 'Welcome to the server'
        server.send_message(welcome_msg, client_address, code=code.CODE_OK)
    elif key == 'time':
        print(key + ' | message: {} | sender: {}:{}'.format(data, client_address[0], client_address[1]))
        server.send_message('', client_address, code=code.CODE_OK)

server.stop()
