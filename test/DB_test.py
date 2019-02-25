import sys
sys.path.append("..")

import unittest
from PartyAppServer.Main import DBInterface


class DB_Test(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_insertUser(self):
        DB = DBInterface.DBInterface(
            DBInterface.TinyDB_PlaylistHandler(),
            DBInterface.TinyDB_SongHandler(),
            DBInterface.TinyDB_UserHandler(),
            DBInterface.TinyDB_SearchHandler()
        )
        DB.UserDB.DB.purge_tables()
        res = DB.UserDB.new_user('asdkjlfbasdfu3')
        self.assertIsNot(res, 0)
        
 



if __name__ == '__main__':
    unittest.main()
