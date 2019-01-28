import socket
import time

TCP_IP = '10.0.255.36'
TCP_PORT = 50007

BUFFER_SIZE = 1024

running = True
counter = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

MESSAG = b'UA#AC:AD:AC:AD:AD:CD'
s.send(MESSAG)
data = s.recv(1024)

print(data)

MESSAG = b'HA#1231#AC:ED:AC:AD:AD:CD'
s.send(MESSAG)
data = s.recv(1024)

print(data)

MESSAG = b'UA#AC:AD:AC:AD:AD:FD'
s.send(MESSAG)
data = s.recv(1024)

print(data)