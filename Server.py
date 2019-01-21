import socket
import threading

MyIP = 'localhost'
MyPort = 9778

BUFFER_SIZE = 1024
HOST_PW = '1234'
MAX_CONN = 10

host_found = False
server_running = True

Server = None

def setup():
    global Server, MyIP, MyPort, MAX_CONN
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Conndata = (MyIP, MyPort)
    Server.Bind(Conndata)