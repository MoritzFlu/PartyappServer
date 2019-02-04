import mysql.connector as mariadb
from tinydb import *

from abc import ABC, abstractmethod
import re

class DBInterface(ABC):

    def exec_command(cmd, vals):
        pass

    @abstractmethod
    def get_user(self, ID):
        pass

    #@abstractmethod
    def new_user(self, MAC):
        pass

    #@abstractmethod
    def get_playlist():
        pass


class TinyDB_Interface(DBInterface):
    UserDB = None
    SongsDB = None
    PlaylistDB = None

    def __init__(self):
        self.UserDB = TinyDB('DB/users.json')
        self.UserDB.purge_tables()
        self.SongsDB = TinyDB('DB/songs.json')
        self.PlaylistDB = TinyDB('DB/playlist.json')

    

    def insert_user(self, ID, MAC, Points, isHost=False):
        self.UserDB.insert(
            {'ID': ID, 'MAC': MAC, 'Points': Points, 'isHost': isHost})

    def get_user(self, ID):
        res = self.UserDB.search(where('ID') == ID)
        if res == []:
            return 0
        return res[0]['ID']

    def new_user(self, MAC):
        res = self.UserDB.search(where('MAC') == MAC)
        isHost = False

        if res == []:
            users = self.UserDB.all()
            start = 1

            for user in users:
                if user['ID'] == start:
                    start = user['ID'] + 1

            myID = start
            isHost = False
            if myID == 1:
                isHost = True

            # add new user
            self.insert_user(myID, MAC, 0, isHost=isHost)
        else:
            myID = res[0]['ID']

        return myID   # return ID to Server

    def get_playlist(self):
        res = self.PlaylistDB.all()
        return res

    def search_song(self, Name, Interpret):

        def wildcard_match(val, compVal):
            if compVal in val:
                return True
            else:
                return False


        res = None
        if Name != None and Interpret != None:
            res = self.PlaylistDB.search(where('Name').test(wildcard_match,Name) & where('Interpret').test(wildcard_match,Interpret))
        if Name != None and Interpret == None:
            res = self.PlaylistDB.search(where('Name').test(wildcard_match,Name))
        if Name == None and Interpret != None:
            res = self.PlaylistDB.search(where('Interpret').test(wildcard_match,Interpret))
        if Name == None and Interpret == None:
            return None
        return res

  

