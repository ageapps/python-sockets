# Socket Management in `python`

Some examples of uses of `udp` and `tcp` sockets in `python`.

This includes also a small framework to use sockets in an easy way using a custom protocol.
The framework includes 3 main abstractions:

+ `protocol`: this class defines the way packets are coded and decoded, transmitted and received, independently of the transport protocol (tcp or udp).
+ `client`: this class is a generic client that handles sending and receiving messages. It can be configured to use udp or tcp.
+ `server`: this class needs to be developed according to the user needs and transport protocol wanted. 

Both `client` and `server` classes use the `protocol` class to be compatible.



## Resources

+ http://stupidpythonideas.blogspot.com/2013/05/sockets-are-byte-streams-not-message.html
+ https://www.studytonight.com/network-programming-in-python/blocking-and-nonblocking-socket-io
+ https://realpython.com/python-sockets/
+ https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ
+ https://docs.python.org/2/library/socket.html
