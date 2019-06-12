import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from protocol import BasicProtocol
from LogManager import getLogger


class Client(object):

    def __init__(self, port: int, host="127.0.0.1", udp=False, protocol=None, debug=False, timeout=5):
        self.host = host
        self.port = port
        self.udp = udp
        self.logger = getLogger(__name__, debug)
        if protocol is None:
            protocol = BasicProtocol(debug=debug)
        self.protocol = protocol
        socket_kind = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
        try:
            s = socket.socket(socket.AF_INET, socket_kind)
            s.settimeout(timeout)
            if not udp:
                s.connect((self.host, self.port))
            self.logger.info('Starting {} socket | host: {}:{} | protocol: {}'.format(('UDP' if udp else 'TCP'), self.host, self.port, self.protocol.__class__.__name__))
        except socket.error as err:
            self.logger.error('Failed to start socket | Error: {}'.format(err))
            raise

        self.client_socket = s
        self.receiver_fn = s.recvfrom if udp else s.recv

    def send_message(self, message, wait_answer=False):
        fragments = self.protocol.get_messages_to_send(message)
        sent = 0
        for msg in fragments:
            try:
                if self.udp:
                    sent += self.client_socket.sendto(msg, (self.host, self.port))
                else:
                    sent += self.client_socket.sendall(msg)
            except socket.error as err:
                self.logger.error('Failed send message | Error: {}'.format(err))
                raise
            if sent <= 0:
                raise Exception('Failed sending message {}'.format(msg))

        if wait_answer:
            answer, address = self.receive_message()
            if address != (self.host, self.port):
                raise Exception(
                    "Error sending answer | Sender: {} Answer: {}".format((self.host, self.port), address))
            return answer
        else:
            return sent

    def receive_message(self):
        return self.protocol.receive_from_socket(self.receiver_fn)

    def stop(self):
        self.client_socket.close()
