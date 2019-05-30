from protocol import BasicProtocol
from protocol import code
import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


class UDPRServer(object):
    '''UDP Reliable Server

    Arguments::
        port {int} -- port to expose in host

    Keyword Arguments::
        host {str} -- specify host to expose the server (default: {"127.0.0.1"})
        protocol {Protocol} -- Protocol to be used from the server (default: {BasicProtocol()})
    '''

    def __init__(self, port,  host="127.0.0.1", protocol=BasicProtocol()):
        self.host = host
        self.port = port
        self.protocol = protocol

    def start(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((self.host, self.port))
            print("UDP socket listening on {}:{}".format(self.host, self.port))
        except socket.error as err:
            print('Failed to start socket | Error: {}'.format(err))
            raise

        self.server_socket = s
        self.protocol.set_receiver(s.recvfrom)

    def get_formated_message(self, msg, key, code=0):
        msg = {
            'data': msg,
            'key': key,
            'code': code
            }
        return msg

    def receive_message(self, send_answer=False, answer_msg=None):
        """receive message

        Keyword Arguments:
            send_answer {bool} -- true if sending an answer is needed (default: {False})
            answer_msg {Object} -- message to send (default: {None})

        Returns:
            dict{data: Object, code: int} -- data and response code
            address -- addres from sender
        """
        msg, address = self.protocol.receive()

        if send_answer:
            if answer_msg is None:
                answer_msg = self.get_formated_message('', '', code.CODE_OK)
            sent = self.send_message(answer_msg, address, wait_answer=False)
            if not sent:
                raise Exception("Error sending answer")
        
        return msg, address

    def send_message(self, msg, destination, wait_answer=False, key='', code=0):
        msg = self.get_formated_message(msg, key, code)
        fragments = self.protocol.get_messages_to_send(msg)
        correct = False
        for msg in fragments:
            try:
                b_sent = self.server_socket.sendto(msg, destination)
                correct = correct and (b_sent > 0)
            except socket.error as err:
                print('Failed send message | Error: {}'.format(err))
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
