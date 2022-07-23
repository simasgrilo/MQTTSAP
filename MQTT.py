
import paho.mqtt.client as mqttClient
import mqtt_client as MQTTSAP
import ssl
import random
import time
import json

class MqttSap(MQTTSAP.PahoMQTT):

    def __init__(self,clientID,certificateFile,secret):

        super(MqttSap,self).__init__(client_id=clientID)
        self.serverURL = '29cf1730-34da-4b38-9edd-30be889be55f.eu10.cp.iot.sap'
        self.port = 8883
        self.clientID = clientID
        self.topic = "measures/" + clientID
        self.topicSubscribe = "ack/" + clientID
        self.certificateFile = certificateFile
        self.secret = secret

    def onConnect(self,client: mqttClient,uesrdata,flags,rc):
        """Defines a callback to the on_connection event. Translates the Return code to the corresponding
        Error message as defined in the OASIS document for MQTTv3.1.

        Parameters:
            client: Paho.mqtt.Client: MQTT client
            Userdata: data sent from the user client to the server
            Flags: control flags sent during the connection process
            rc: return code. sentr from the server denoting whether the connection was successful or not.
            """

        rcDescriptions = {
            1: "Connection Refused: Unacceptable protocol version",
            10: "Timeout waiting for SUBACK",
            11: "Timeout waiting for UNSUBACK",
            12: "Timeout waiting for PINGRESP",
            13: "Malformed Remaining Length",
            14: "Problem with the underlying communication port",
            15: "Address could not be parsed",
            16: "Malformed received MQTT packet",
            17: "Subscription failure",
            18: "Payload decoding failure",
            19: "Failed to compile a Decoder",
            2: "Connection Refused: Identifier rejected",
            3: "Connection Refused: Server Unavailable",
            4: "Connection Refused: Bad username or password",
            5: "Connection Refused: Authorization error",
            6: "Connection lost or bad"
        }
        if not rc:
            print("Connected: Return code = " + str(rc))
        else:
            print("Not connected: Return code is " + str(rc) + ": "
                  "{}".format(rcDescriptions.get(rc)))

    def onMessage(self,userdata,message,message_recv):
        """Callback method to process messages received from the broker whenever a message for the topic regarding the
        measurement data which the current client is subscribed (i.e., 'measures/<device_alternate_id>').

        Parameters:
            userdata: data sent by the user to the broker
            message_recv: Message received from the broker

        Prints success message, if the message was successfully posted to the server. otherwise, it shoes
        the error cause of why the messages was not processed successfully in the server.

        """
        print("Message received in main topic:")
        parsedMessage = json.loads(message_recv.payload.decode("utf-8"))
        if parsedMessage[0]["code"] == 200 or parsedMessage[0]["code"] == 202:
            print("Message sent successfully to sensor {}".format(parsedMessage[0]["sensorAlternateId"]))
        elif parsedMessage[0]["code"] == 400:
            print("Message is malformed and therefore rejected by the server. The reasons are:")
            for row in range(0,len(parsedMessage[0]["messages"])):
                print(parsedMessage[0]["messages"][row])

    def onCommand(self,client,userdata,message):
        print("Broker:")
        print(message)

    def onError(self,userdata,report):
        print("Error message: ")
        print(report)

    def onSubscribe(self,userdata,message,x,y):
        print("Subscription sucessful!")

    def connect(self):
        """instantiates a client object from class mqtt_client.py"""

        client = MQTTSAP.MQTTClient(device_alternate_id=self.clientID,
                                    instance=self.serverURL,
                                    secret=self.secret,
                                    pemfile=self.certificateFile)
        client.on_connect = self.onConnect
        client.on_command = self.onCommand
        client.on_message = self.onMessage
        client.on_error = self.onError
        client.on_subscribe = self.onSubscribe

        try:
            client.tls_set(pemfile=self.certificateFile,secret=self.secret)
        except ValueError:
            print("TLS already set for this connection")
        except FileNotFoundError:
            raise ValueError("Insert a valid .pem file")
        client.connect()
        client.message_callback_add(self.topicSubscribe, self.onMessage)
        client.subscribe(device_alternate_id=self.clientID)

        return client

    def subscribe(self,device_alternate_id):
        """subscribes to the topic related to the current device. This enables the system to receive and verify error messages,
        if any.

        Parameters:
            device_alternate_id : str -> Alternate ID of the device that data is being sent to Iot Cockpit

        :return A subscription status object.

        """
        measures = 'measures/' + device_alternate_id
        self.message_callback_add(measures, self._command_message_handler)
        return mqttClient.Client.subscribe(measures, 1)

    def processMeasures(self,measures) -> dict:
        """Process measures to deal with multiple measures as defined in SAP standards:
        :param measures : str -> a string containing comma-separated measures"""
        measures = measures[0].split(";")
        resultingJSON = {}
        for measure in measures:
            measure = measure.strip(" {}").split(":")
            measure[0] = measure[0].strip(" ")
            resultingJSON[measure[0]] = float(measure[1])
        return resultingJSON

    def processMeasuresNoName(self,measures):
        """Process measures to deal with multiple measures as defined in SAP standards:
        :param measures : str -> a string containing comma-separated measures in array of arrays-style"""
        measures = measures[0].split(";")
        resultingJSON = []
        for measure in measures:
            resultingJSON.append(float(measure.strip(" [").strip("]")))
        return resultingJSON

    def publish(self,client,capAltId,sensorAltId,measure,timestamp,simulateDelay,simulateValues,textEdit):
        #while True:
        if simulateDelay:
            time.sleep(1)
        message = {
            "capability_alternate_id" : capAltId,
            "sensor_alternate_id" : sensorAltId,
            #"measures": [self.processMeasuresNoName(measures=measure)]
            "measures": [self.processMeasures(measures=measure)]
        }
        if simulateValues:
            message["measures"] = [[random.randint(1,60)]]
        result = client.publish(capability_alternate_id=message["capability_alternate_id"],
                                sensor_alternate_id=message["sensor_alternate_id"],
                                measures=message["measures"],
                                timestamp=timestamp)
        status = result[0]
        if not status:
            print(f"Send "+ str(message["measures"]) + f" to topic `{self.topic}`")
            textEdit.append(f"Send "+ str(message["measures"]) + f" to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
            textEdit.append(f"Failed to send message to topic {self.topic}")

    def runMQTT(self,capAltId,sensorAltId,measure,timestamp,simulateDelay,simulateValues):
        """Executes the simulation of an IoT device feeding SAP with data in a "forever" fashion.

        Parameters:
            capAltId: str -> the equipment's capability alternate ID to which the measure being posted belongs to.
            sensorAltId: str -> the equipment's sensor that is measuring the data
            timestamp: int -> time instant the sensor has measured the data sent to the server

        """
        client = self.connect()
        client.loop_start()
        while True:
            self.publish(client,capAltId,sensorAltId,measure,timestamp,simulateDelay,simulateValues)

    def sendSingleData(self,capAltId,sensorAltId,measure,timestamp,simulateDelay, textEdit):
        """Sends a single piece of data to SAP Broker. This method will be used when loading
        measurement data from an excel file, which will send each value at a time"""
        client = self.connect()
        client.loop_start()
        self.publish(client,capAltId,sensorAltId,measure,timestamp,simulateDelay,False,textEdit)
        client.loop_stop()



