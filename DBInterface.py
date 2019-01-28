import mysql.connector as mariadb

def exec_command(cmd, vals):

    # Structure:
    # cmd contains raw command with %s for vars
    # vals contains vars to insert, format: (var1, var2,)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # ! NO QUOTATION MARKS INSIDE OF THE COMMAND    !
    # ! THOSE ARE PLACE AUTOMATICALLY               !
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    DBUser = 'DBInterface'
    DBPW = '1231'

    DBLink = mariadb.connect(user=DBUser, password=DBPW, database='partyapp') # connect to DB
    DBCursor = DBLink.cursor()  # create cursor for commands
    
    myres = None
    DBCursor.execute(cmd, vals) # execute cmd

    for result in DBCursor:
        myres = result  # get result

    DBLink.commit() # save changes
    DBLink.close() # close connection

    return myres


def get_user(ID):
    CMD = 'Select * from Users where ID = %s'
    VALS = (ID,)
    Result = exec_command(CMD, VALS)

    if Result is None or Result[0] is None:
        return 0

    return Result[0]
        
def new_user(MAC, isHost):          # tries to create new User in DB, if exits returns that ID
                                    # else, creates new Entry and returns new ID

    CMD = 'Select ID from Users Where MAC = %s'
    VALS = (MAC,)
    Result = exec_command(CMD, VALS)

    if Result is None or Result[0] is None:
        CMD = 'Select max(ID) from Users'
        VALS = ()
        Result = exec_command(CMD, VALS)                              # get highest ID
       
        if Result[0] is None:
            myID = 1
        else:
            myID = Result[0] + 1

        CMD = 'Insert Into Users(ID, MAC, isHost) values (%s, %s, %s)'  # add new user
        VALS = (myID, MAC, isHost,)
        Result = exec_command(CMD, VALS)

    else:
        myID = Result[0]

    return myID   # return ID to Server

