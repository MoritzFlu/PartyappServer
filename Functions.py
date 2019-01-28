from abc import ABC
import DBInterface







class TCP_function(ABC):
    ident = ''                  # Entry in first Field used to identify Function
    fields = 0                  # Amount of Fields after first Field
    hostNeeded = False          # Only executable by Host
    
    @abstractmethod
    def run(raw_data):          # initiate data handling
        pass

    def get_ident():            # return ident for comparison
        return self.ident

    def check_host():           # always activated, compares user to hostNeeded
        # DOTO: Check if User is Host
        return True

class TCP_HostAuthentication(TCP_function):
    ident = 'HA'
    fields = 2                  # hostPW, MAC
    hostNeeded = False
    hostPW = ''

    def __init__(hostPW):
        self.hostPW = hostPW
        pass
    
    def run(data):
        if len(data) != self.fields:
            break
        
        if data[0] == self.hostPW:
            ID = DBInterface.new_user(data[1])
            return ID

        else:
            return False

class TCP_UserAuthentication(TCP_function):
    ident = 'UA'
    fields = 1
    hostNeeded = False

    def run(data):
        if len(data) != self.fields:
            break
        ID = DBInterface.new_user(data[1])
        return ID
