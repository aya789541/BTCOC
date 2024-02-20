from clientThread import MqttClient
import time



Broker_IP ="10.198.105.230"
broker_Port = 1883
client = MqttClient(BrokerIP=Broker_IP, BrokerPort=broker_Port, channel="/vehicule", tls_enable=False, Auth_enable=False, publish_enable=True, id=2)
client.setLocation([44.806465, -0.603128])
client.connect_to_Broker()
client.Subscribe_to_channel()
client.start()

time.sleep(20)

client.stop()