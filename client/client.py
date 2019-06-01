import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from protocol import BasicProtocol


class Client(object):

    def __init__(self, port: int, host="127.0.0.1", udp=False, protocol=None, debug=False, timeout=5):
        self.host = host
        self.port = port
        self.udp = udp
        if protocol is None:
            protocol = BasicProtocol(debug=debug)
        self.protocol = protocol
        socket_kind = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
        try:
            s = socket.socket(socket.AF_INET, socket_kind)
            s.settimeout(timeout)
            if not udp:
                s.connect((self.host, self.port))
            print('Starting socket | protocol: ' + self.protocol.__class__.__name__)
        except socket.error as err:
            print('Failed to start socket | Error: {}'.format(err))
            raise

        self.client_socket = s
        self.receiver_fn = s.recvfrom if udp else s.recv

    def send_message(self, message, wait_answer=False):
        fragments = self.protocol.get_messages_to_send(message)
        for msg in fragments:
            try:
                if self.udp:
                    self.client_socket.sendto(msg, (self.host, self.port))
                else:
                    self.client_socket.sendall(msg)
            except socket.error as err:
                print('Failed send message | Error: {}'.format(err))
                raise

        if wait_answer:
            answer, address = self.receive_message()
            if  self.udp and address == (self.host, self.port):
                raise Exception(
                    "Error sending answer | Sender: {} Answer: {}".format((self.host, self.port), address))
            return answer

    def receive_message(self):
        return self.protocol.receive_from_socket(self.receiver_fn)
