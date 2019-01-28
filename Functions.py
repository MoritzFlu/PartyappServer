import abc
import DBInterface
from abc import ABC

# These Functions will be used automaticall by the server so all the code
# needed for a Function must be implemented here
# If the server has to send an answer, the functions needs to return 
# an array containing those Messages

# NEEDS TO BE FIRST FUNCTION!
class TCP_function(ABC):
    ident = ''                  # Entry in first Field used to identify Function
    fields = 0                  # Amount of Fields after first Field
    hostNeeded = False          # Only executable by Host
    
    @abc.abstractmethod
    def run(raw_data):          # initiate data handling
        pass

    def get_ident(self):            # return ident for comparison
        return self.ident

    def check_host(self):           # always activated, compares user to hostNeeded
        # DOTO: Check if User is Host
        return True


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ! ADD FUNCTIONS STARTING HERE !
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class TCP_HostAuthentication(TCP_function):
    ident = 'HA'
    answerIdent = 'AA'

    fields = 2                  # hostPW, MAC
    hostNeeded = False
    hostPW = '1231'
    
    def run(self,data):
        if len(data) != self.fields:
            i = 1
        
        if data[0] == self.hostPW:
            ID = DBInterface.new_user(data[1], True)
        else:
            ID = 0

        MSG = '{}#{}'.format(self.answerIdent, ID)
        return MSG

class TCP_UserAuthentication(TCP_function):

    ident = 'UA'
    answerIdent = 'AA'

    fields = 1          # MAC
    hostNeeded = False

    def run(self,data):

        if len(data) != self.fields:
            i = 1

        Host = DBInterface.get_user(1)

        if Host == 1:
            ID = DBInterface.new_user(data[0], False)
        else:
            ID = 0
        
        MSG = '{}#{}'.format(self.answerIdent, ID)

        return MSG
