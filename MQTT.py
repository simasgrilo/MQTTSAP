
import paho.mqtt.client as mqttClient
import random
import iot_services_sdk.mqtt_client as MQTTSAP
import ssl
import time

class MqttSap(MQTTSAP.PahoMQTT):

    def __init__(self,clientID,certificateFile,secret):

        self.serverURL = '29cf1730-34da-4b38-9edd-30be889be55f.eu10.cp.iot.sap'
        self.port = 8883
        self.clientID = clientID
        self.topic = "measures/" + clientID
        self.topicSubscribe = "ack/" + clientID
        self.certificateFile = certificateFile
        self.keyStore = "./certificates/client.ks"
        self.secret = secret

    def onConnect(self,client: mqttClient,uesrdata,flags,rc):
        print("Connected: Return code = " + str(rc))

    def onMessage(self,userdata,message):
        print("Message received in main topic:")
        print(message)

    def onCommand(self,client,userdata,message):
        print("Broker:")
        print(message)

    def onError(self,userdata,report,a):
        print("Error message: ")
        print(report)

    def connect(self):
        client = MQTTSAP.MQTTClient(device_alternate_id=self.clientID,
                                    instance=self.serverURL,
                                    secret=self.secret,
                                    pemfile=self.certificateFile)
        client.on_connect = self.onConnect
        client.on_command = self.onCommand
        client.on_message = self.onMessage
        client.on_error = self.onError

        try:
            client.tls_set(pemfile=self.certificateFile,secret=self.secret)
        except ValueError:
            print("TLS already set for this connection")
        client.connect()
        client.subscribe(device_alternate_id=self.clientID)
        return client


    def publish(self,client,capAltId,SensorAltId):
        while True:
            time.sleep(10)
            result = client.publish(capability_alternate_id="[BRA] Air conditioning",
                                    sensor_alternate_id="BRA_Air_conditioning",
                                    measures=[[random.randint(1,60)]])
            print(result)
            status = result[0]
            if status == 0:
                print(f"Send 'message' to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")


    def runMQTT(self):
        client = self.connect()
        client.loop_start()
        for _ in range(0,10):
            self.publish(client,"BRA_Air_conditioning","[BRA] Air conditioning")
        client.loop_stop()


