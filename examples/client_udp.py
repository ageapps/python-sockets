import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from client import Client
from protocol import BasicProtocol
from protocol import code


HOST = "localhost"
PORT = 12344
QUEUE_SIZE = 5
UDP_CLIENT = True
HEADER_SIZE = 20


def get_formated_message(msg, key, code=0):
    msg = {
        'data': msg,
        'key': key,
        'code': code
        }
    return msg


def main():
    proto = BasicProtocol()
    client = Client(PORT, host=HOST, udp=UDP_CLIENT, protocol=proto)
    hello_message = get_formated_message('Hello server','setup')
    answer = client.send_message(hello_message, wait_answer=True)
    if answer['code'] != code.CODE_OK:
        print('Error in response')
        sys.exit()
    elif answer['code'] == code.CODE_OK:
        print('Successfully joined | server: {}:{}'.format(HOST,PORT))

    while True:
        time.sleep(2)
        new_msg = get_formated_message( time.time(), 'time')
        answer = client.send_message(new_msg, wait_answer=True)
        if answer['code'] != code.CODE_OK:
            print('Error in response')
            client.stop()
            sys.exit()

    client.stop()

if __name__ == '__main__':
    main()
