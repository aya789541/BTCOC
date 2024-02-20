#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt
import os
import threading
                                                                ## Prepare the path of certs ##
Path = os.getcwd()
Cert_Path = os.path.join(Path, "MQTTClient","mosquitto", "certs", "CA")
Client_Certificate_Path = os.path.join(Path, "MQTTClient","mosquitto", "certs", "ClientCertificates")


                                                                ## Choose Port
def Client_Key_File(KeyType):
    return os.path.join(Client_Certificate_Path, KeyType, "client.pem")

def Client_Certificate_File(KeyType):
    return os.path.join(Client_Certificate_Path, KeyType, "client.crt")
    


def Choose_Port(Encrypt, Auth, keyType=None):
    if Encrypt == False:
        if Auth:
            return 1884
        else:
            return 1883
    else:
        if keyType == "Curve448":
            if Auth:
                return 8884
            else:
                return 8883
        elif keyType == "P-256":
            if Auth:
                return 8886
            else:
                return 8885
        elif keyType == "RSA_256":
            if Auth:
                return 8888
            else:
                return 8887
        elif keyType == "RSA_512":
            if Auth:
                return 8890
            else:
                return 8889
        elif keyType == "RSA_1024":
            if Auth:
                return 8892
            else:
                return 8891
    # If no matching keyType is found, return None or raise an exception as needed.
    return None  # You can modify this to fit your specific use case.


                                                                ## Format number
def latitude_format(coord):
    rounded_coord = "{:.7f}".format(coord)


    integer_part, fractional_part = rounded_coord.split('.')

    padded_integer_part = integer_part.zfill(3)

    padded_fractional_part = fractional_part.ljust(7, '0')

    formatted_coord = padded_integer_part + '.' + padded_fractional_part

    return formatted_coord

def longitude_format(coord):
    rounded_coord = "{:.7f}".format(coord)

    integer_part, fractional_part = rounded_coord.split('.')

    padded_integer_part = integer_part.zfill(4)

    padded_fractional_part = fractional_part.ljust(7, '0')

    formatted_coord = padded_integer_part + '.' + padded_fractional_part

    return formatted_coord


def Speed_format(nombre):
    formatted_number = "{:.1f}".format(float(nombre))

    integer_part, fractional_part = formatted_number.split('.')

    padded_integer_part = integer_part.zfill(3)

    formatted_speed = padded_integer_part + '.' + fractional_part

    return formatted_speed

def Client_ID_format(nombre, length=4):
    # Formater la partie entière avec la longueur spécifiée
    partie_entiere_formattee = "{:0{}}".format(int(nombre), length)
    return partie_entiere_formattee

def Time_format(nombre):
    # Formater la partie entière avec trois chiffres
    partie_entiere_formattee = "{:010d}".format(int(nombre))

    # Formater la partie décimale avec huit chiffres après la virgule
    partie_decimale_formattee = "{:.7f}".format(nombre - int(nombre))

    # Retourner la chaîne formatée
    return partie_entiere_formattee + partie_decimale_formattee[1:]

                                                                       ## MQTT client ##   
class MqttClient(threading.Thread):
    def __init__(self, BrokerIP, channel ,tls_enable, Auth_enable, id ,username=None, password=None, Test=False, frequency = 10, stayAliveIntervale = 1, ClientKeyType="RSA_256", ServerKeyType="RSA_256"):
        # Thread initialize
        threading.Thread.__init__(self)

        # Create a mqtt client instance
        self.client = mqtt.Client()

        # Broker infos
        self.BrokerIP = BrokerIP
        self.BrokerPort = Choose_Port(Encrypt=tls_enable, Auth=Auth_enable, keyType=ServerKeyType)
        self.channel = channel
        self.stayAliveIntervale = stayAliveIntervale
        self.frequency = frequency
        self.id = Client_ID_format(id, 4)
        # Client infos
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onTestMessage if Test else  self.onLocationMessage
        self.publish = self.Publish_to_channel_Test if Test else self.Publish_to_channel_location

        self.latency_data = []  # liste pour stocker les temps d'envoi     
        self.connection_data = [] # 
        self.clientView = {}

        # Client state
        self.connected = False
        self.Terminated = False
        self.connecting = False
        self.connectioState = ""

        # Client position & speed
        self.Location = ["-91.0000000", "0000.0000000"]
        self.speed = "000.0"

        # Will message
        self.client.will_set(channel, payload=f"-91.0000000,0000.0000000,{self.speed},{self.id}", qos=2, retain=False)

        if (tls_enable):
            self.client.tls_set(ca_certs=os.path.join(Cert_Path, "ca.crt"), certfile=Client_Certificate_File(ClientKeyType), keyfile=Client_Key_File(ClientKeyType))
            self.client.tls_insecure_set(True) # indique au client MQTT de ne pas vérifier si le certificat du serveur MQTT est émis par une autorité de certification (CA) de confiance 
        # Set username and password
        if (Auth_enable):
            self.client.username_pw_set(username, password)


    def setSpeed(self, speed):
        self.speed = Speed_format(speed)

    def getSpeed(self):
        return self.speed
    
    def getLocation(self):
        return self.Location
    
    def setLocation(self, newLocation):
        if newLocation!= self.Location:
            self.Location = [latitude_format(newLocation[0]), longitude_format(newLocation[1])]

    def get_View(self):
        return self.clientView
    
    def run(self):
        self.Publish_With_Frequence()

    def stop(self):
        self.Terminated = True
        self.disconnect_from_Broker()

    def connect_to_Broker(self):
        self.connecting = True
        self.connection_data.append(time.time())
        try : 
            self.client.connect(self.BrokerIP , self.BrokerPort, self.stayAliveIntervale)
        except Exception as e:
            self.connecting = False
            self.connectioState = e
            print(e)

        self.client.loop_start()
        while self.connecting==True:
                continue
        
    
    def disconnect_from_Broker(self):
        self.connected = False
        msg = f"-91.0000000,0000.0000000,{self.speed},{self.id}"
        self.client.publish(self.channel, msg, qos=2)
        self.client.disconnect()

    def Subscribe_to_channel(self):
        self.client.subscribe(self.channel, qos=2)
    
    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connection_data.append(time.time())
            self.connected = True
        else: 
            print(f"Connection failed with return code {rc}")
        self.connecting = False
    
    def calculate_connection_time(self):
        if not self.connection_data:
            print("Aucune donnée de connection disponible.")
            return None 
        return self.connection_data[1] - self.connection_data[0]

        
    def calculate_average_latency(self):

        if not self.latency_data:
            print("Aucune donnée de latence disponible.")
            return None

        total_latency = sum(self.latency_data)
        average_latency = total_latency / len(self.latency_data)

        # print(f"Latence moyenne pour tous les messages : {average_latency} secondes")
        return average_latency

    def Publish_to_channel_location(self):
        msg = f"{self.Location[0]},{self.Location[1]},{self.speed},{self.id}"
        self.client.publish(self.channel, msg, qos=2)

    def Publish_to_channel_Test(self):
        _time = Time_format(time.time()) # length 18 avec client ID de length 5 + 2 commas => 25 la taille du message et de 35
        msg_to_send = f"{_time},{self.id},"
        msg_to_send = msg_to_send.ljust(35, '0')
        self.client.publish(self.channel, msg_to_send, qos=2)
    
    def onLocationMessage(self, client, userdata, msg):
        longitude, latitude, speed, client_id = msg.payload.decode().split(',')
        if client_id!=self.id:
            
            if float(longitude) == -91:
                if self.clientView[client_id]:
                    del self.clientView[client_id]
                print(self.clientView)
            else : 
                self.clientView[client_id] = {"location" : [longitude, latitude], "speed":speed}
                print(self.clientView)
                

       

    def onTestMessage(self, client, userdata, msg):
        _time = time.time()
        _Sending_Time, client_id , _ = msg.payload.decode().split(',')

        if client_id == self.id:
            # print(f"Received message value: {received_msg}")
            _Sending_Time = float(_Sending_Time)

            # Calculer la latence
            latency = _time - _Sending_Time

            # Stocker la latence dans le dictionnaire
            #with self.lock:
            self.latency_data.append(latency)
        
    def Publish_With_Frequence(self):
        while not self.Terminated and self.connected:
            #print(self.Terminated)
            self.publish()
            time.sleep(1/self.frequency)



