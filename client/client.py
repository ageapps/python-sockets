import socket
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from protocol import BasicProtocol

class Client(object):

    def __init__(self, port, host="127.0.0.1", udp=False, protocol=BasicProtocol()):
        self.host = host
        self.port = port
        self.udp = udp
        self.protocol = protocol
        socket_kind = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
        try:
            s = socket.socket(socket.AF_INET, socket_kind)
            if not udp:
                s.connect((self.host, self.port))
        except socket.error as err:
            print('Failed to start socket | Error: {}'.format(err))
            sys.exit()

        self.client_socket = s
        receiver = s.recvfrom if udp else s.recv
        self.protocol.set_receiver(receiver)
 

    def send_message(self, message):
        fragments = self.protocol.get_messages_to_send(message)
        for msg in fragments:
            try:
                if self.udp:

                    self.client_socket.sendto(msg, (self.host, self.port))
                else:
                    self.client_socket.sendall(msg)
            except socket.error as err:
                print('Failed send message | Error: {}'.format(err))
                sys.exit()

    def receive_message(self):
        msg, address = self.protocol.receive()
        return {"data": msg}, address
