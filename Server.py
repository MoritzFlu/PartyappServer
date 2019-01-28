import socket
import threading

import json
import abc
import Functions
import DBInterface

# Server Data
HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

# Constants
BUFFER_SIZE = 1024
HOST_PW = '1234'
USER_AUTH_TAG = 'UA'
HOST_AUTH_TAG = 'HA'
MSG_DELIMITER = "#"
DECODING_CODE = 'utf-8'

CFG_PATH = "ServerCfg.json"
KNOWN_PATH = "knownClients.json"

# System Management Vars
host_found = False
server_running = True

# Main Socket Server
Server = None
Clients = []
TCP_Functions = []


        


def setup():
    init_functions()
    CMD = 'DELETE FROM USERS'
    VALS = ()
    DBInterface.exec_command(CMD, VALS)
    while server_running:
        server()

def format_data(data):
    global DECODING_CODE
    data = data.decode(DECODING_CODE) 
    data = decrypt_data(data)
    data_array = data.split(MSG_DELIMITER)
    return data_array

def decrypt_data(data):
    return data

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
        res = handle_data(data)         # pass to next function

        if not res is None:
            if isinstance(res,list):
                for msg in res:
                    b_msg = str.encode(msg)
                    conn.send(b_msg)
            else:
                b_msg = str.encode(res)
                conn.send(b_msg)

    conn.close()                        # Transmission complete

def handle_data(data):
    global TCP_Functions
    data_arr = format_data(data)
    res = None

    for func in TCP_Functions:
        ident = func.get_ident()
        if data_arr[0] == ident:
            data_arr.remove(ident)
            res = func.run(data_arr)
            break

    if not res is None:
        return res

    

def init_functions():
    global TCP_Functions

    start = False                       # If True, Instances are created in next Loop
    firstFunction = 'TCP_function'      # Wont be used, starting with the next class 

    # iterate over all Functions in Module Function
    for name, clss in Functions.__dict__.items():

        if start:

            # If Flag is set, create instance
            module = __import__('Functions')
            class_ = getattr(module, name)
            instance = class_()

            # Append to List
            TCP_Functions.append(instance)

        if name == firstFunction:

            # Add instances starting next loop
            start = True



setup()



