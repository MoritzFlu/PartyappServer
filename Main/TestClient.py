import socket
import time
import random
import string

TCP_IP = '10.0.255.36'
TCP_PORT = 50007

BUFFER_SIZE = 1024

running = True
counter = 0

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    searching = True
    while searching:
        try:
            s.connect((TCP_IP, TCP_PORT))
            searching = False
        except:
            continue
    return s



s = connect()

MESSAG = b'HA#1231#AC:ED:AC:AD:AD:CD'
s.send(MESSAG)
data = s.recv(1024)
print(data)

s = None

s = connect()

MESSAG = b'SS#2#1'
s.send(MESSAG)

receiving = True
totalData = ''
while receiving:
    try:
        data = s.recv(1024)
        data = data.decode("utf-8")
        totalData = totalData + data
    except:
        receiving = False
print(totalData)

    