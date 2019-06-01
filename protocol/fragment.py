import json
import socket
class FragmentProtocol(object):
    """ Protocol based on  max_packet_size in bytes

    The packet has the following structure

    |           DATA        | FRAGMENT FLAG |
    |   max_packet_size-1   |     1         |
    """
    def __init__(self, max_packet_size=1024, encoding='utf-8', debug=False):
        self.max_packet_size = max_packet_size
        self.encoding = encoding
        self.fragmented_flag = 1
        self.debug = debug

    def encode(self, msg: str) -> bytes:
        if self.debug:
            print("Encoding: {}".format(msg))
        assert isinstance(msg, str) , "Type of msg should be str: {}".format(type(msg))
        return bytes(msg, self.encoding)

    def get_messages_to_send(self, msg) -> list:
        if not isinstance(msg, str):
            msg = json.dumps(msg)
                
        msg_bytes = bytearray(self.encode(msg))
        fragments = []
        if len(msg_bytes) <= (self.max_packet_size-1):
            fragments.append(bytes(msg_bytes))
        else:
            while msg_bytes:
                # fragment message
                bytes_to_send = msg_bytes[:(self.max_packet_size-1)]

                if len(msg_bytes) > (self.max_packet_size-1):
                    # set fragmented byte
                    bytes_to_send.append(self.fragmented_flag)

                assert (len(bytes_to_send) <= self.max_packet_size), "Size of fragment is not correct".format(len(bytes_to_send))
                fragments.append(bytes(bytes_to_send))
                msg_bytes = msg_bytes[(self.max_packet_size-1):]
        
        if self.debug:
            print("Sending fragments: {}".format(fragments))
        return fragments

    def decode(self, msg_bytes: bytes) -> object:
        msg = str(msg_bytes.decode(self.encoding)).strip()
        if msg[0] == "{" or msg[0] == "[":
            msg = json.loads(msg)
        
        return msg
    

    def receive_packet(self, receive_fn):
        result = receive_fn(self.max_packet_size)

        address = None
        if isinstance(result, tuple):
            msg, address = result
        else:
            msg = result
        
        return msg, address

    def receive_from_socket(self, receive_fn) -> (object, tuple):
        """receive message using the given function by the client/server
        
        Raises:
            Exception: Receiving
        
        Returns:
            (data, address)
        """

        data_b = bytearray()
        address = None
        while True:
            # get header
            msg_bytes, address = self.receive_packet(receive_fn)
            if not len(msg_bytes):
                raise Exception("Error receiving packet: {}".format(msg_bytes))
                return
            
            msg_array = bytearray(msg_bytes)
            if self.debug:
                print("Received | bytes:{} | data:{}".format(len(msg_array), msg_bytes))
            
            flag = 0
            if len(msg_array) == self.max_packet_size:
                flag = msg_array[len(msg_array)-1]
                data = msg_array[:len(msg_array)-1]
            else:
                data = msg_array

            data_b += data # concatenate data
            if (flag != self.fragmented_flag):
                break
                
        data = self.decode(bytes(data_b))
        return data, address
