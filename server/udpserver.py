import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from protocol import BasicProtocol
from LogManager import getLogger

class UDPServer(object):
    '''UDP Reliable Server

    Arguments::
        port {int} -- port to expose in host

    Keyword Arguments::
        host {str} -- specify host to expose the server (default: {"127.0.0.1"})
        protocol {Protocol} -- Protocol to be used from the server (default: {BasicProtocol()})
    '''

    def __init__(self, port,  host="127.0.0.1", debug=False, protocol=None):
        self.host = host
        self.port = port
        self.logger = getLogger(__name__, debug)
        
        if protocol is None:
            protocol = BasicProtocol(debug=debug)
        self.protocol = protocol

    def start(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((self.host, self.port))
            self.logger.info('UDP socket listening on {}:{} | protocol: {}'.format(self.host, self.port, self.protocol.__class__.__name__))
        except socket.error as err:
            self.logger.error('Failed to start socket | Error: {}'.format(err))
            raise

        self.server_socket = s

    def receive_message(self, send_answer=False, answer_msg=''):
        """receive message

        Keyword Arguments:
            send_answer {bool} -- true if sending an answer is needed (default: {False})
            answer_msg {Object} -- message to send (default: {None})

        Returns:
            dict{data: Object} -- data
            address -- addres from sender
        """

        msg, address = self.protocol.receive_from_socket(self.server_socket.recvfrom)

        if send_answer:
            sent = self.send_message(answer_msg, address, wait_answer=False)
            if not sent:
                raise Exception("Error sending answer")
        
        return msg, address

    def send_message(self, msg, destination: tuple, wait_answer=False):
        fragments = self.protocol.get_messages_to_send(msg)
        correct = True
        for msg in fragments:
            try:
                b_sent = self.server_socket.sendto(msg, destination)
                correct = correct and (b_sent > 0)
            except socket.error as err:
                self.logger.error('Failed send message | Error: {}'.format(err))
                raise
        
        if wait_answer:
            answer, address = self.receive_message(send_answer=False)
            if address == destination:
                raise Exception("Error sending answer | Sender: {} Answer: {}".format(destination, address))
            return answer
        else:
            return correct

    def stop(self):
        self.server_socket.close()
