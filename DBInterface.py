import mysql.connector as mariadb
from abc import ABC, abstractmethod

class DBInterface(ABC):

    @abstractmethod
    def exec_command(cmd, vals):
        pass

    @abstractmethod
    def get_user(self, ID):
        pass

    @abstractmethod
    def new_user(self, MAC):
        pass

    @abstractmethod
    def get_playlist():
        pass



class Maria_Interface(DBInterface):
    DBUser = 'DBInterface'
    DBPW = '1231'

    DBLink = None

    def __init__(self):
        self.DBLink = mariadb.connect(user=self.DBUser, password=self.DBPW, database='partyapp') # connect to DB

    def exec_command(self, cmd, vals):

        # Structure:
        # cmd contains raw command with %s for vars
        # vals contains vars to insert, format: (var1, var2,)
        
        # Example:
        # CMD = 'SELECT * FROM USERS WHERE ID = %s AND MAC like %s'
        # VALS = (ID,MAC,)
        # exec_command(CMD, VALS)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ! NO QUOTATION MARKS INSIDE OF THE COMMAND    !
        # ! THOSE ARE PLACE AUTOMATICALLY               !
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        
        myres = []
        
        DBCursor = self.DBLink.cursor()  # create cursor for commands
        DBCursor._buffered = True
         
        try:
            DBCursor.execute(cmd, vals) # execute cmd  
            for row in DBCursor:
                print(row)
                myres.append(row)
        except: 
            myres = []
     


        self.DBLink.commit() # save changes
        DBCursor.close()
        DBCursor = None

        return myres


    def get_user(self, ID):
        CMD = 'Select * from Users where ID = %s'
        VALS = (ID,)
        Result = self.exec_command(CMD, VALS)

        if Result == []:
            return 0

        return Result[0]
            
    def new_user(self, MAC):          # tries to create new User in DB, if exits returns that ID
                                        # else, creates new Entry and returns new ID

        CMD = 'Select ID from Users Where MAC = %s'
        VALS = (MAC,)
        Result = self.exec_command(CMD, VALS)
        isHost = False

        if Result == []:
            CMD = 'Select max(ID) from Users'
            VALS = ()
            Result = self.exec_command(CMD, VALS)                              # get highest ID
        
            if Result == [] or Result[0][0] == None:
                myID = 1
                isHost = True
            else:
                myID = Result[0][0] + 1

            CMD = 'Insert Into Users(ID, MAC, isHost) values (%s, %s, %s)'  # add new user
            VALS = (myID, MAC, isHost,)
            Result =self. exec_command(CMD, VALS)

        else:
            myID = Result[0][0]

        return myID   # return ID to Server

    def get_playlist(self):

        CMD = 'Select * from playlist order by curpoints asc'
        VALS = ()
        Result = self.exec_command(CMD, VALS)

        return Result

