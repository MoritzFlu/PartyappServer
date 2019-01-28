import socket
import threading
from Client import User, Host, UserThread, HostThread
import json
import abc
import Functions

# Server Data
HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

# Constants
BUFFER_SIZE = 1024
HOST_PW = '1234'
USER_AUTH_TAG = 'UA'
HOST_AUTH_TAG = 'HA'
MSG_DELIMITER = '#'
DECODING_CODE = 'utf-8'

CFG_PATH = "ServerCfg.json"
KNOWN_PATH = "knownClients.json"

# System Management Vars
host_found = False
server_running = True

# Main Socket Server
Server = None
Clients = []

def load_cfg():
    global BUFFER_SIZE, HOST_PW, USER_AUTH_TAG, HOST_AUTH_TAG, MSG_DELIMITER, DECODING_CODE, CFG_PATH
    try:
        json_data = open(CFG_PATH).read()
        data = json.loads(json_data)

        BUFFER_SIZE = int(data['BUFFER_SIZE'])
        HOST_PW = data['HOST_PW']
        USER_AUTH_TAG = data['USER_AUTH_TAG']
        HOST_AUTH_TAG = data['HOST_AUTH_TAG']
        MSG_DELIMITER = data['MSG_DELIMITER']
        DECODING_CODE = data['DECODING_CODE']

    except:
        break


def setup():
    load_cfg()
    Functions.init_DB()
    while server_running:
        server()

def open_socket():
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        print(af, socktype, proto, canonname, sa)

        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue

        try:
            s.bind(sa)
            print(sa)
            s.listen(1)

        except socket.error as msg:
            s.close()
            s = None
            continue
        break

    return s

def server():
    global BUFFER_SIZE, HOST, PORT
    
    s = open_socket()                   # Wait for conenction, return connection

    if s is None:                       # If connection already closed
        print('could not open socket')

    conn, addr = s.accept()             # conn is object, addr is array with ip + port
    print('Connected by', addr)

    listening = True                    # flag to allow terminating on next loop

    while listening:
        data = conn.recv(BUFFER_SIZE)   # receiving Data, max size in BUFFER_SIZE
        if not data: break              # connection closed, no data received
        handle_data(data)               # pass to next function

    conn.close()                        # Transmission complete

def handle_data(data):
    print(data)








