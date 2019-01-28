import socket
import time
import random
import string

TCP_IP = '10.0.255.36'
TCP_PORT = 50007

BUFFER_SIZE = 1024

running = True
counter = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

MESSAG = b'HA#1231#AC:ED:AC:AD:AD:CD'
s.send(MESSAG)
data = s.recv(1024)
print(data)
s.close()

for x in range(100):
    time.sleep(0.5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    MESSAG = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
    MESSAG = 'UA#' + MESSAG
    MESSAG = str.encode(MESSAG)
    try:
        s.send(MESSAG)
        data = s.recv(1024)
        print(data)
    except:
        continue
    s.close()
