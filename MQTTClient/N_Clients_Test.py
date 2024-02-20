from clientThread import MqttClient
from time import sleep

# Paramètres du mosquitto broker 
BrokerIP = "10.168.130.226"
channel = "/vehicule"
frequency = 10


# userParametre

N = int(input("Number of clients you want : "))
Encrypt = True if input("Encryption ( yes : 1, no : 0 or leave it blank) : ") == "1" else False
Auth = True if input("Authentication ( yes : 1, no : 0 or leave it blank) : ") == "1" else False
Username = input("Username : ") or "zineb"
Password = input("Password : ") or "zineb"

# To choose the right port to connect 

if Encrypt and Auth :
    BrokerPort = 8884
elif Encrypt :
    BrokerPort = 8883
elif Auth:
    BrokerPort = 1884
else:
    BrokerPort = 1883

# BrokerIP, BrokerPort, channel,tls_enable, Auth_enable, username=None, password=None, frequency = 10
Clients = [MqttClient(BrokerIP, BrokerPort, channel, Encrypt, Auth, True,str(i), Username, Password) for i in range(N)]

for client in Clients:
    client.start()

sleep(2)
for client in Clients:
    client.stop()
    average = client.calculate_average_latency()
    connect_time = round(client.calculate_average_connection_time(), 6)
    print(f"|==| Average : {average}, connect_time : {connect_time}")
