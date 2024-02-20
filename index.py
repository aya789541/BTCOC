# coding: utf-8
import eel
import sys
import gc
from time import sleep
# appending a path
sys.path.append('./MQTTClient')

from clientThread import MqttClient

class User():
    def __init__(self, location = None, connected = False):
        self.location = location
        self.connected = connected
    def SetLocation(self, location):
        self.location = location

    def SetConnection(self, connected):
        self.connected = connected
    
    def getLocation(self):
        return self.location
    
    def getConnection(self):
        return self.connected


global Client, BrokerIP, Username, Password, Encryption, Authentication, Client_key, Server_key, Client_Key_Types, Server_Key_Types, Test_Client_keys, Test_Server_keys

Test_Client_keys = []
Test_Server_keys = []
Client_Key_Types = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]
Server_Key_Types = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]
Client_key = "RSA_256"
Server_key = "RSA_256"
BrokerIP = ""
Username= ""
Password = ""
Encryption = False
Authentication = False
Client = None
Average_rounds = 10
X_labels = []
Connection_Times = []



@eel.expose
def getConnection_Times():
    global Connection_Times
    return Connection_Times

@eel.expose
def getX_labels():
    global X_labels
    return X_labels

                                        ## Connection Time Test ##

@eel.expose
def Connection_Time_Test():
    global BrokerIP, Test_Client_keys, Test_Server_keys, Average_rounds, X_labels, Connection_Times
    X_labels = []
    Connection_Times = []
    for client_key_type in Test_Client_keys:
        for server_key_type in Test_Server_keys:
            X_labels.append(f"client_{client_key_type}\nserver_{server_key_type}")
            connection_time = 0
            for _ in range(Average_rounds):
                Client = MqttClient(BrokerIP=BrokerIP, channel="/vehicule", tls_enable=True, Auth_enable=Authentication, id=1, username="zineb", password="zineb", ClientKeyType=client_key_type, ServerKeyType=server_key_type)
                Client.connect_to_Broker()
                connection_time+= Client.calculate_connection_time()
                Client.disconnect_from_Broker()
                del Client
                gc.collect()
            Connection_Times.append(connection_time/float(Average_rounds))


                                       ################      Client      #############

def Initialize_Client():
    global Client, BrokerIP, Username, Password, Encryption, Authentication
    if not Client:
        Client = MqttClient(BrokerIP = BrokerIP,channel="/vehicule",
                            tls_enable=Encryption, Auth_enable=Authentication, id=1,
                            username=Username, password=Password, Test=False, ClientKeyType=Client_key, ServerKeyType=Server_key)

    
@eel.expose
def getClientKeyTypes():
    global Client_Key_Types
    return Client_Key_Types

@eel.expose
def getServerKeyTypes():
    global Server_Key_Types
    return Server_Key_Types
                                                                    ###### Conenction Test #########
@eel.expose
def getTest_Client_keys():
    global Test_Client_keys
    return Test_Client_keys

@eel.expose
def getTest_Server_keys():
    global Test_Server_keys
    return Test_Server_keys

@eel.expose
def setTest_Client_keys(choosedClientKeys):
    global Test_Client_keys
    Test_Client_keys = choosedClientKeys

@eel.expose
def setTest_Server_keys(choosedServerKeys):
    global Test_Server_keys
    Test_Server_keys = choosedServerKeys

@eel.expose
def Connect_Client():
    global Client
    if not Client : 
        Initialize_Client()
    if is_Connected() == False:
        Client.connect_to_Broker()
        Client.Subscribe_to_channel()
        Start_publishing()
    return ""

@eel.expose
def Start_publishing():
    global Client
    if Client:
        Client.start()

@eel.expose 
def is_Connected():
    if Client:
        return Client.connected
    return False

@eel.expose
def disconnecte_Client():
    global Client
    if not Client : 
        Initialize_Client()

    if is_Connected() == True:
        Client.stop()
        Client = None
    return ""

@eel.expose
def Set_position(cords):
    if Client:
        Client.setLocation(cords)

@eel.expose
def Get_Vehiculs_Location():
    if Client:
        return Client.get_View()
    return {}

                                       ################      ENCRYPTION      #############
@eel.expose
def setEncryption(value):
    global Encryption
    Encryption = value

@eel.expose
def getEncryption():
    return Encryption

                                       ################      Authentication      #############
@eel.expose
def setAuthentication(value):
    global Authentication
    Authentication = value

@eel.expose
def getAuthentication():
    return Authentication

                                       ################      BrokerIP      #############
@eel.expose
def getBrokerIP():
    return BrokerIP

@eel.expose
def setBrokerIP(brokerIP):
    global BrokerIP
    BrokerIP = brokerIP


                                       ################      Username      #############
@eel.expose
def getUsername():
    return Username

@eel.expose
def setUsername(username):
    global Username
    Username = username

                                       ################      Password      #############
@eel.expose
def getPassword():
    return Password

@eel.expose
def setPassword(password):
    global Password
    Password = password


                                       ################      Option      #############

@eel.expose
def setKeyType(KeyType, target):
    if target =="Client":
        global Client_key
        Client_key = KeyType
    elif target == "Server":
        global Server_key
        Server_key = KeyType

@eel.expose
def getKeyType(target):
    if target=="Client":
        global Client_key
        return Client_key
    elif target=="Server":
        global Server_key
        return Server_key


if __name__ == '__main__':

    if sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)
    else:
        eel.init('build')
        eel.start('index.html')
