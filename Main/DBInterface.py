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

    @abstractmethod
    def new_user(self, UUID):
        pass

    @abstractmethod
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

    

    def insert_user(self, ID, UUID, Points, isHost=False):
        self.UserDB.insert(
            {'ID': ID, 'UUID': UUID, 'Points': Points, 'isHost': isHost})

    def get_user(self, ID):
        res = self.UserDB.search(where('ID') == ID)
        if res == []:
            return 0
        return res[0]['ID']

    def get_points(self, ID):
        try:
            res = self.UserDB.search(where('ID') == int(ID))
            return res[0]['Points']
        except:
            return 0

    def new_user(self, UUID):
        res = self.UserDB.search(where('UUID') == UUID)
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
            self.insert_user(myID, UUID, 0, isHost=isHost)
        else:
            myID = res[0]['ID']

        return myID   # return ID to Server

    def get_playlist(self):
        res = self.PlaylistDB.all()
        songs = []
        for song in res:
            entry = self.SongsDB.search(where('ID') == int(song['ID']))
            songs.append(entry[0])
        return res

    def search_song(self, searchVal):

        def wildcard_match(val, compVal):
            if compVal in val:
                return True
            else:
                return False

        res = self.SongsDB.search(
            where('Interpret').test(wildcard_match,searchVal) |
            where('Titel').test(wildcard_match, searchVal)
        )

        return res

    def add_song(self, ID):

        res = self.PlaylistDB.search(where('ID') == int(ID))
        if res == []:
            # Song not found, add to Playlist
            newSong = self.SongsDB.search(where('ID') == int(ID))
            song = {}
            song['ID'] = newSong[0]['ID']
            song['CurPoints'] = 0
            self.PlaylistDB.insert(song)
        else:
            # Song Found, add 1 Point
            self.PlaylistDB.update(increment('CurPoints'), where('ID') == int(ID))
        return 1

    def sub_points(self, ID, val):
        try:
            self.UserDB.update(subtract('Points', val), where('ID') == int(ID))
            return 1
        except:
            return 0
        
            
