import socket
import threading
from Client import User, Host

# Server Data
MyIP = ''
MyPort = 9778

# Constants
BUFFER_SIZE = 1024
HOST_PW = '1234'
MAX_CONN = 10

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
    print(name, pname)
    newcl.close()


def acceptConnection(newcl, addr):
    global Clients



def startThread():
    i = 0

setup()
p = Host('1', '1', '1')
while server_running:
    mainLoop()
