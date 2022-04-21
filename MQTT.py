import certifi
import paho.mqtt.publish as mqttPublish
import paho.mqtt.client as mqttClient
import random
import ssl
import time

class MqttSap():

    def __init__(self,clientID,certificateFile):
        self.serverURL = '29cf1730-34da-4b38-9edd-30be889be55f.eu10.cp.iot.sap'
        self.port = 8883
        self.clientID = clientID
        self.topic = "measures/" + clientID
        self.topicSubscribe = "ack/" + clientID
        self.certificateFile = certificateFile

    def onConnect(self,client: mqttClient,uesrdata,flags,rc):
        print("Conectado: código de retorno = " + str(rc))
        client.subscribe(topic=self.topicSubscribe)

    def connect(self):
        client = mqttClient.Client(client_id=self.clientID)
        client.on_connect = self.onConnect
        #print(certifi.where())
        client.tls_set(
                       certfile=self.certificateFile,
                       cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None
        )
        client.connect(host=self.serverURL, port=self.port, keepalive=60)
        client.subscribe(topic=self.topicSubscribe)
        return client

    def publish(self,client):
        while True:
            message = str({"capabilityAlternateId": "[BRA] Air conditioning",
               "sensorAlternateId": "BRA_Air_conditioning",
               "measures": [[random.randint(1, 60)]]
               })
            time.sleep(3000)
            result = client.publish(self.topic, message)
            print(result)
            status = result[0]
            if status == 0:
                print(f"Send '{message}' to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")

    def runMQTT(self):
        client = self.connect()
        #client.loop_forever()
        client.loop_start()
        self.publish(client)



