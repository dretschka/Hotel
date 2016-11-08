import socket

s = socket.socket()
s.bind(localhost, 8080)

s.listen(5)