import time
from clientThread import MqttClient, Choose_Port

# Paramètres du mosquitto broker 
BrokerIP = "192.168.43.63"
channel = "/vehicule"
frequency = 10


# userParametre

Encrypt = True if input("Encryption ( yes : 1, no : 0 or leave it blank) : ") == "1" else False
Auth = True if input("Authentication ( yes : 1, no : 0 or leave it blank) : ") == "1" else False
Username = input("Username : ") or "zineb"
Password = input("Password : ") or "zineb"

client = MqttClient(BrokerIP=BrokerIP, channel=channel, tls_enable=Encrypt, Auth_enable=Auth, Test=False, id=2, username=Username, password=Password, ClientKeyType="RSA_256", ServerKeyType="RSA_256")
client.connect_to_Broker()
client.Subscribe_to_channel()
client.setSpeed(0)
client.setLocation([15.0, 0.0])
client.start()
time.sleep(20)
client.disconnect_from_Broker()
print(client.calculate_connection_time())