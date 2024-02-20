from clientThread import MqttClient
from time import sleep

Broker_IP = "192.168.43.63"
channel = "/vehicule"

Key_Types = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]
auth_enable = True


for client_key_type in Key_Types:
    for server_key_type in Key_Types:
        Client = MqttClient(BrokerIP=Broker_IP, channel=channel, tls_enable=True, Auth_enable=auth_enable, id=1, username="zineb", password="zineb", ClientKeyType=client_key_type, ServerKeyType=server_key_type, Test=True)
        Client.connect_to_Broker()
        Client.Subscribe_to_channel()
        Client.start()
        sleep(10)
        Client.stop()
        latency = Client.calculate_average_latency()
        print(f"Client key type : {client_key_type}, Server key type : {server_key_type}, latency : {latency}")