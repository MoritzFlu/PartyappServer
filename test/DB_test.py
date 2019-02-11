import sys
sys.path.append("..")

import unittest
from PartyAppServer.Main import DBInterface


class DB_Test(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_insertUser(self):
        # Setup
        DB = DBInterface.TinyDB_Interface()
        DB.UserDB.purge_tables()

        # Vals
        ID = 1
        Uname = 'TestIdent'
        Points = 5
        isHost = True

        # Test
        DB.insert_user(ID, Uname, Points, isHost=isHost)

        # fetch Result
        Res = DB.get_user(ID)

        # assert
        self.assertEqual(ID, Res)
        
    def test_addUser(self):
        # Setupt
        DB = DBInterface.TinyDB_Interface()
        DB.UserDB.purge_tables()

        # Vals
        Uname = 'TestIdent'


        # Test
        ID = DB.new_user(Uname)

        #fetch Result
        Res = DB.get_user(ID)

        # assert
        self.assertEqual(ID, Res)

    def test_getPlaylist(self):
        # Setupt
        DB = DBInterface.TinyDB_Interface()
        DB.PlaylistDB.purge_tables()

        ID = 1
        Points = 5

        DB.PlaylistDB.insert(
            {
                'ID': ID,
                'Points': Points
            }
        )

        res = DB.get_playlist()
        length = len(res)

        self.assertIsNot(length,0)

    def test_searchSong(self):
        DB = DBInterface.TinyDB_Interface()
        DB.SongsDB.purge_tables()

        ID = 1
        Titel = 'MeinTitel'
        Interpret = 'Mein Interpret'
        Pfad = 'I  C:\\ you :)'

        DB.SongsDB.insert(
            {'ID': ID,
             'Titel': Titel,
             'Interpret': Interpret,
             'Pfad': Pfad
            }
        )

        res = DB.search_song(Interpret)
        leng = len(res)
        self.assertIsNot(0, leng)




if __name__ == '__main__':
    unittest.main()
