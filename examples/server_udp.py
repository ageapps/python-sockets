import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from server import UDPServer
from protocol import FragmentProtocol
from protocol import code

PORT = 12344
HOST = ''
UDP_SERVER = True
HEADER_SIZE = 20

def get_formated_message(msg, key, code=0):
    msg = {
        'data': msg,
        'key': key,
        'code': code
        }
    return msg


def main():
    proto = FragmentProtocol()

    server = UDPServer(PORT, protocol=proto)
    server.start()

    while True:
        msg, client_address = server.receive_message(send_answer=False)
        data = msg['data']
        key = msg['key']
        if key == 'setup':
            print(key + ' | message: {} | sender: {}:{}'.format(data, client_address[0], client_address[1]))
            welcome_msg = get_formated_message('Welcome to the server',key, code=code.CODE_OK)
            server.send_message(welcome_msg, client_address)
        elif key == 'time':
            print(key + ' | message: {} | sender: {}:{}'.format(data, client_address[0], client_address[1]))
            msg = get_formated_message('', key, code=code.CODE_OK)
            server.send_message(msg, client_address)

    server.stop()


if __name__ == '__main__':
    main()
