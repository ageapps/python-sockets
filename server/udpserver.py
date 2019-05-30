import socket
import sys
from protocol import BasicProtocol


class UDPServer(object):
    def __init__(self, port,  host="127.0.0.1", protocol=BasicProtocol(), queue_size=5):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.queue_size = queue_size

    def start(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((self.host, self.port))
            print("UDP socket listening on {}:{}".format(self.host, self.port))
        except socket.error as err:
            print('Failed to start socket | Error: {}'.format(err))
            sys.exit()

        self.server_socket = s
        self.protocol.set_receiver(s.recvfrom)


    def receive_message(self):
        msg, address = self.protocol.receive()
        return {"data": msg}, address

    def send_message(self, msg, destination):
        fragments = self.protocol.get_messages_to_send(msg)
        for msg in fragments:
          try:
              self.server_socket.sendto(msg, destination)
          except socket.error as err:
              print('Failed send message | Error: {}'.format(err))
              sys.exit()

    
    def stop(self):
        self.server_socket.close()
