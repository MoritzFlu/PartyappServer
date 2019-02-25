import mysql.connector as mariadb
from tinydb import *

from abc import ABC, abstractmethod
import re


###################     DB Handler Abstrac Classes      ###########################

# DB that contains all playable songs
class SongDB_Handler(ABC):
    DB = None

    @abstractmethod
    def __init__(self):
        pass

# DB that contains active Playlist
class PlaylistDB_Handler(ABC):
    DB = None

    @abstractmethod
    def __init__(self):
        pass

# DB that contains list of all known users
class UserDB_Handler(ABC):
    DB = None

    @abstractmethod
    def __init__(self):
        pass

# DB that contains the recent search results for ID
class SearchDB_Handler(ABC):
    DB = None

    @abstractmethod
    def __init__(self):
        pass
########################################################################


########################################################################
#                                                                      #
#                   Main Interface Implementation                      #
#                                                                      #
########################################################################

class DBInterface():
    SearchDB = None
    PlaylistDB = None
    SongDB = None
    UserDB = None

    def __init__(self, PlaylistDB, SongDB, UserDB, SearchDB):
        self.PlaylistDB = PlaylistDB
        self.SongDB = SongDB
        self.UserDB = UserDB
        self.SearchDB = SearchDB

    def search(self, term, ID):
        res = self.SongDB.search_song(term)
        songs = self.SearchDB.insert_results(ID, res)
        return songs

    def add_song(self, SongID, ClientID):
        song = self.SearchDB.get_song_viaID(SongID)
        real_song = self.SongDB.fetch_using_artist_title(song['artist'],song['title'])
        self.PlaylistDB.add_song(real_song['Artist'], real_song['Title'])
    
    def add_points_to_user(self, UserID, Points):
        self.UserDB.add_points(UserID, Points)

    def new_user(self, UUID):
        res = self.UserDB.new_user(UUID)
        return res

    def check_for_host(self):
        res = self.UserDB.get_user_viaID(1)
        if res == []:
            return 0
        else:
            return 1

    def get_points(self, ClientID):
        res = self.UserDB.get_points_viaID(ClientID)
        return res

########################################################################
#                                                                      #
#                   TinyDB Handlers                                    #
#                                                                      #
########################################################################

class TinyDB_SearchHandler(SearchDB_Handler):

    ID_STRING = 'ID'
    TITLE_STRING = 'Title'
    ARTIST_STRING = 'Artist'
    PATH = 'DB/search.json'

    DB = None

    # Create DB handler
    def __init__(self):
        self.DB = TinyDB(self.PATH)

    # called to insert entry
    def insert_song(self, song):
        self.DB.insert(song)

    # Will read list of songs, append them to DB and return with IDs
    def insert_results(self, ClientID, Songs):
        searched = self.DB.table(str(ClientID))
        res = []
        for song in Songs:
            ID = len(searched.all())
            new = {
                ID_STRING:ID,
                TITLE_STRING:song[TITLE_STRING],
                ARTIST_STRING:song[ARTIST_STRING]
            }
            searched.insert(new)
            res.append(new)
        return res        

    def get_song_viaID(self, ID):
        searched = self.DB.table(str(ClientID))
        res = searched.search(where('ID') == ID)
        return res

    # Clears Table of Client identified by ClientID
    def clear_table(self, ClientID):
        self.DB.purge_table(str(ClientID))

class TinyDB_SongHandler(SongDB_Handler):
    
    Artist_STRING = 'Artist'
    TITLE_STRING = 'Title'
    PATH = 'DB/songs.json'


    def __init__(self):
        self.DB = TinyDB(self.PATH)

    def insert_song(self, Title, Artist, Path):
        song = {
            'Title':Title,
            'Artist':Artist,
            'Path':Path
        }
        self.DB.insert(song)

    # Serach song via keyword, return results
    def search_song(self, keyword):

        # function used to test if keyword in Field
        def wildcard_match(val, compVal):
            if compVal in val:
                return True
            else:
                return False

        # search the DB
        res = self.DB.search(
            where(self.Artist_STRING).test(wildcard_match,keyword) |
            where(self.TITLE_STRING).test(wildcard_match, keyword)
        )

        return res

    def fetch_using_artist_title(self, artist, title):
        res = self.DB.search(
            where(self.Artist_STRING) == artist &
            where(self.TITLE_STRING) == title
        )
        return res

class TinyDB_UserHandler(UserDB_Handler):

    PATH = 'DB/users.json'

    # Field Structure in DB Table
    UUID_FIELD = 'UUID'
    ID_FIELD = 'ID'
    POINTS_FIELD = 'Points'
    HOST_Field = 'isHost'

    DB = None

    def __init__(self):
        self.DB = TinyDB(self.PATH)

    def new_user(self, UUID):
        
        # Check if user already in DB
        res = None
        res = self.get_user_viaUUID(UUID)

        if res == []:
            # get amount of entries = new ID
            ID = len(self.DB.all()) + 1

            if ID == 1:
                # first User is Host
                self.insert_user(UUID, ID, isHost=True)
            else:  
                self.insert_user(UUID, ID)
            return ID

        else:
            return res[0]['ID']
    
    def insert_user(self, UUID, ID, isHost=False):

        USER = {
            self.UUID_FIELD:UUID,
            self.ID_FIELD:ID,
            self.POINTS_FIELD:0,
            self.HOST_Field:isHost
        }
        self.DB.insert(USER)

    def add_points(self, UserID, Points):
        self.DB.update(add('Points', Points), ID == UserID)

    def get_user_viaID(self, ID):
        res = self.DB.search(where(self.ID_FIELD) == int(ID))
        if res == []:
            return 0
        else:
            return res['ID']
    
    def get_points_viaID(self, ID):
        res = self.DB.search(where(self.ID_FIELD) == int(ID))
        if res == []:
            return 0
        else:
            return res['Points']

    def get_user_viaUUID(self, UUID):
        res = self.DB.search(where(self.UUID_FIELD) == UUID)
        return res

class TinyDB_PlaylistHandler(PlaylistDB_Handler):
    PATH = 'DB/playlist.json'

    DB = None

    def __init__(self):
        self.DB = TinyDB(self.PATH)

    def add_points(self, Points, SongID):
        self.DB.update(add('Points', Points), ID == SongID)

    def add_song(self, Artist, Title):
        contained = self.DB.search(where('Artits') == Artist & where('Title') == Title)
        if contained == []:
            ID = len(self.DB.all())
            song = {
                'ID':ID,
                'Title':Title,
                'Artist':Artist,
                'Points':0
            }
            self.DB.insert(song)
        else:
            self.add_points(1, contained['ID'])

    def get_playlist(self):
        res = self.DB.all()
        return res




