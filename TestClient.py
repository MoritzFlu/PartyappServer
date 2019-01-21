import socket
import time

TCP_IP = '10.0.255.36'
TCP_PORT = 9778

BUFFER_SIZE = 1024

running = True
counter = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

MESSAG = b'HA#1234'
s.send(MESSAG)

while running:

    
    
    print("Sending: {}".format(MESSAG))
    s.send(b'aaaaaaaabbbb')
    time.sleep(2)
    counter += 1

    if counter > 20:
        running = False