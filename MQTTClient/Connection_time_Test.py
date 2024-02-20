from clientThread import MqttClient
from time import sleep
import matplotlib.pyplot as plt
import gc

Broker_IP = "10.198.105.230"
channel = "/vehicule"
Client_Types = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]
Server_Types = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]

def Connection_Time_Test():
    auth_enable = True
    Average_rounds = 10
    X_labels = []
    Connection_Times = []

    global Broker_IP, channel, Client_Types, Server_Types
    for client_key_type in Client_Types:
        for server_key_type in Server_Types:
            X_labels.append(f"client_{client_key_type}\nserver_{server_key_type}")
            connection_time = 0
            for _ in range(Average_rounds):
                Client = MqttClient(BrokerIP=Broker_IP, channel=channel, tls_enable=True, Auth_enable=auth_enable, id=1, username="zineb", password="zineb", ClientKeyType=client_key_type, ServerKeyType=server_key_type)
                Client.connect_to_Broker()
                connection_time+= Client.calculate_connection_time()
                Client.disconnect_from_Broker()
                del Client
                gc.collect()

            Connection_Times.append(connection_time/float(Average_rounds))
    return X_labels, Connection_Times





print(Connection_Time_Test())