import abc
from DBInterface import *
from abc import ABC

# These Functions will be used automaticall by the server so all the code
# needed for a Function must be implemented here
# If the server has to send an answer, the functions needs to return 
# an array containing those Messages

# NEEDS TO BE FIRST FUNCTION!
class TCP_function(ABC):
    ident = ''                  # Entry in first Field used to identify Function
    fields = 0                  # Amount of Fields needed in data in for run
    hostNeeded = False          # Only executable by Host
    DB = None

    def __init__(self, DB):             # Create DB Connection
        self.DB = DB

    @abc.abstractmethod
    def run(self, raw_data):          # initiate data handling
        pass

    def get_ident(self):            # return ident for comparison
        return self.ident

    def check_host(self):           # always activated, compares user to hostNeeded
        # DOTO: Check if User is Host
        return True
    
    def check_data(self, data):
        if len(data) != self.fields:
            return False
        return True


    


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ! ADD FUNCTIONS STARTING HERE !
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class TCP_HostAuthentication(TCP_function): # checked
    ident = 'HA'
    answerIdent = 'AA'

    fields = 2                  # hostPW, UUID
    hostNeeded = False
    hostPW = '1231'
    
    def run(self,data):
        # More fields than necessary DOTO: handling
        if  not self.check_data(data):
            return

        # Check if host pw correct
        if data[0] == self.hostPW:
            # Add Host
            UUID = data[1]
            ID = self.DB.new_user(UUID)
        else:
            ID = 0

        # Return Message
        MSG = '{}#{}'.format(self.answerIdent, ID)
        return MSG

class TCP_UserAuthentication(TCP_function): # checked
    ident = 'UA'
    answerIdent = 'AA'

    fields = 1          # UUID
    hostNeeded = False

    def run(self,data):
        
        # More fields than necessary DOTO: handling
        if  not self.check_data(data):
            return

        # Check if Host exists
        Host = self.DB.check_for_host()

        if Host == 1:
            # Add Host to Users
            ID = self.DB.new_user(data[0])
        else:
            # No Host, return Error
            ID = 0
        
        # Return Message
        MSG = '{}#{}'.format(self.answerIdent, ID)
        return MSG

class TCP_FetchPlaylist(TCP_function):      # checked
    ident = 'PR'
    answerIdentSignal = 'PS'
    answerIdentEntry = 'PE'

    fields = 1
    hostNeeded = False

    def run(self, data):
       # More fields than necessary DOTO: handling
        if  not self.check_data(data):
            return
        MSG = []
        
        if data[0] == '1':
            Songs = self.DB.PlaylistDB.get_playlist()
            MSG.append(self.answerIdentSignal + '#1')

            # 0: ID
            # 1: CurPoints
            # 2: Name
            # 3: Interpret

            for s in Songs:
                MSG.append('{}#{}#{}#{}#{}'.format(self.answerIdentEntry, s['ID'], s['Points'], s['Title'], s['Artist']))
            MSG.append(self.answerIdentSignal + '#0')

        return MSG

class TCP_SearchSong(TCP_function):         # checked
    ident = 'SS'
    answerIdentSignal = 'ST'
    answerIdentEntry = 'SE'
    fields = 2   # Search Value, ClientID
    hostNeeded = False


    def run(self, data):
        if  not self.check_data(data):
            return

        
        Songs = self.DB.search(data[0], data[1])
        MSG = []
        MSG.append(self.answerIdentSignal + '#1')
        for s in Songs:
            # 0: ID
            # 1: Name
            # 2: Interpreter
            MSG.append('{}#{}#{}#{}'.format(self.answerIdentEntry, s['ID'], s['Title'], s['Artist']))
        MSG.append(self.answerIdentSignal + '#0')
        return MSG

class TCP_RetrievePoints(TCP_function):     # checked

    ident = 'RP'
    fields = 1   # ID
    answerIdent = 'PA'
    hostNeeded = False

    def run(self, data):
        if  not self.check_data(data):
            return
        res = self.DB.get_points(data[0])
        MSG = self.answerIdent + '#' + str(res)
        return MSG

class TCP_AddSong(TCP_function):            # checked

    ident = 'AS'
    fields = 2      # Song ID, ClientID
    hostNeeded = False

    def run(self, data):
        if  not self.check_data(data):
            return
        res = self.DB.add_song(data[0], data[1])
        res = self.DB.add_points_to_user(data[1], -1)
        return 

class TCP_AlterPoints(TCP_function):        # checked

    ident = 'AP'
    fields = 2    # Points, ClientID
    hostNeeded = False

    def run(self, data):
        if  not self.check_data(data):
            return

        try:
            points = int(data[0])
        except:
            return
        
        self.DB.add_points_to_user(data[1], points)
        return

class TCP_VoteSong(TCP_function):           # checked

    ident = 'VS'
    fields = 1          # SongID, ClientID
    hostNeeded = False

    def run(self, data):
        if  not self.check_data(data):
            return
        self.DB.add_song(data[0], data[1])
        return

