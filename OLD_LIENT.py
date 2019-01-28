import socket
import abc
from threading import Thread

# Interface 
class Client(abc.ABC):
    IP = ''
    MAC = ''
    mySocket = None

    IP = ''
    MAC = ''
    mySocket = None
    alive = True
    BUFFER_SIZE = 1024

    def __init__(self, IP, Mac, mySocket):
        self.IP = IP
        self.MAC = Mac
        self.mySocket = mySocket

    def getIP(self):
        return self.IP

    def handleData(self, data):
        print(self.IP, self.MAC, data)

    def decryptData(self, data):
        return data

    def run(self):
        while self.alive:

            try:
                data = self.mySocket.recv(self.BUFFER_SIZE)
            except:
                data = False

            # check if connection alive
            if not data:
                self.alive = False
                break

            new_data = self.decryptData(data)
            self.handleData(new_data)


    

class UserThread(Thread):
    IP = ''
    MAC = ''
    mySocket = None
    myClient = None

    def __init__(self, IP, MAC, mySocket):
        Thread.__init__(self)
        self.IP = IP
        self.MAC = MAC
        self.mySocket = mySocket

    def run(self):
        self.myClient = User(self.IP, self.MAC, self.mySocket)
        self.myClient.run()

class HostThread(Thread):
    IP = ''
    MAC = ''
    mySocket = None
    myClient = None

    def __init__(self, IP, MAC, mySocket):
        Thread.__init__(self)
        self.IP = IP
        self.MAC = MAC
        self.mySocket = mySocket

    def run(self):
        self.myClient = Host(self.IP, self.MAC, self.mySocket)
        self.myClient.run()

class User(Client):
    def __init__(self, IP, MAC, mySocket):
        Client.__init__(self, IP, MAC, mySocket)

    
        

class Host(Client):
    def __init__(self, IP, MAC, mySocket):
        Client.__init__(self, IP, MAC, mySocket)
    

