import importlib
import socket
import Functions
from DBInterface import *

# Server Data
HOST = '0.0.0.0'              # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
server_running = True

# Constants
BUFFER_SIZE = 1024        # MAx size of one message
MSG_DELIMITER = "#"       # Symbol seperating fields of one message
DECODING_CODE = 'utf-8'   # Coding of final String (from bytes)


# Functions loaded from Functions.py
# Every Function after TCP_function from that Module will be added to this
# List. To determine which Function to use for data handling,
# The Functions can be looped over.
TCP_Functions = []


        

# Main Entry
def setup(): 
    init_functions()

    # Main Loop
    s = open_socket()   
    while server_running:
        server(s)

# Take Raw Data, Return Array of Strings
def format_data(data):
    global DECODING_CODE
    # from bytes to string
    data = data.decode(DECODING_CODE) 
    # decrypt
    data = decrypt_data(data)
    # convert to array
    data_array = data.split(MSG_DELIMITER)
    return data_array

# Decrypt raw data, not implemented
def decrypt_data(data):
    return data

# Open a new Socket to accept a user
def open_socket():

    # use all possible interfaces
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):

        af, socktype, proto, canonname, sa = res
        try:
            #create socket
            print(res)
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            # couldnt bind socket, abort
            s = None
            continue

        try:
            #bind to port and await connection
            s.bind(sa)
            s.listen(0)

        except socket.error as msg:
            #if error close
            s.close()
            s = None
            continue
        break

    return s


# Main Server, receving and sending data
def server(s):
    global BUFFER_SIZE, HOST, PORT

    # If connection already closed
    if s is None:                       
        print('could not open socket')  

    # conn is object, addr is array with ip + port
    conn, addr = s.accept()             
    print('Connected by', addr)

    # flag to allow terminating on next loop
    listening = True                    

    while listening:
        try:
            # receiving Data, max size in BUFFER_SIZE
            data = conn.recv(BUFFER_SIZE)   
        except:
            break

        # connection closed, no data received
        if not data: break             
        res = handle_data(data)         

        if not res is None:
            # check if res is a list, otherwise you would loop over every letter
            if isinstance(res,list): 
                # res is list
                for msg in res:
                    b_msg = str.encode(msg)
                    conn.sendall(b_msg)
            else:
                #res is string
                b_msg = str.encode(res)
                conn.send(b_msg)

    # Transmission complete
    conn.close()                        


# Calls correct function based on received Data
def handle_data(data):
    global TCP_Functions

    # Decode string, split into Array
    data_arr = format_data(data)
    res = None

    # Loop over functions
    for func in TCP_Functions:
        ident = func.get_ident()
        if data_arr[0] == ident:
            #if ident = Function ident -> Remove ident from arr and Exec Function
            data_arr.remove(ident)
            res = func.run(data_arr)
            break

    # if Function returns Data, pass it up
    if not res is None:
        return res

    
# This function loads all Functions from the Module Functions, 
# creates an instance and adds it to the global list of TCP_Functions
# This way a function added to that Module will be implemented automatically

def init_functions():
    global TCP_Functions

    
    start = False                       # If True, Instances are created in next Loop
    firstFunction = 'TCP_function'      # Wont be used, starting with the next class 

    DB = init_DB()
    # iterate over all Functions in Module Function
    for name, clss in Functions.__dict__.items():

        if start:

            # If Flag is set, create instance
            module = __import__('Functions')
            class_ = getattr(module, name)
            try:
                instance = class_(DB)
                # Append to List
                TCP_Functions.append(instance)
                
            except:
                continue

        if name == firstFunction:

            # Add instances starting next loop
            start = True

def init_DB():
    DB = TinyDB_Interface()
    return DB


if __name__ == '__main__':
    setup()



