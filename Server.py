import socket
import threading
from Client import User, Host, UserThread, HostThread
import json

# Server Data
MyIP = ''
MyPort = 9778

# Constants
BUFFER_SIZE = 1024
HOST_PW = '1234'
MAX_CONN = 10
USER_AUTH_TAG = 'UA'
HOST_AUTH_TAG = 'HA'
MSG_DELIMITER = '#'
DECODING_CODE = 'utf-8'

# System Management Vars
host_found = False
server_running = True

# Main Socket Server
Server = None
Clients = []



def setup():
    global Server, MyIP, MyPort, MAX_CONN
    MyIP = socket.gethostbyname(socket.gethostname())
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Conndata = (MyIP, MyPort)

    # Bind Socket to Port
    Server.bind(Conndata)

    # Listen for new connections
    Server.listen(MAX_CONN)
    print("Listening on {}:{}".format(MyIP, MyPort))

def mainLoop():
    global Server, Clients

    newcl, addr = Server.accept()
    acceptConnection(newcl, addr)
    


def acceptConnection(newcl, addr):
    global Clients, host_found, USER_AUTH_TAG, HOST_PW, HOST_AUTH_TAG
    if host_found:
        split_data = decompData(newcl)
        if split_data[0] == USER_AUTH_TAG:
            new_client = UserThread(addr[0], split_data[1], newcl)
            Clients.append(new_client)
            new_client.start()
    else:
        split_data = decompData(newcl)
        if split_data[0] == HOST_AUTH_TAG and split_data[1] == HOST_PW:
            new_client = HostThread(addr[0], split_data[1], newcl)
            Clients.append(new_client)
            new_client.start()

def decompData(newcl):
    global BUFFER_SIZE, DECODING_CODE, MSG_DELIMITER
    decData = newcl.recv(BUFFER_SIZE).decode(DECODING_CODE)
    arrData = decData.split(MSG_DELIMITER)
    return arrData

def startThread():
    i = 0

setup()
while server_running:
    mainLoop()
