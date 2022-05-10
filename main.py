from MQTT import MqttSap

#from test import MqttSap

import iot_services_sdk.mqtt_client as mqttSAP
import random

if __name__ == '__main__':
    conn = MqttSap("50B0D0984B17407688F9714CFAFBA6DA",
                   "./certificates/certificate.pem",
                   "zFYhclwBxX#4ntETy#cZA7Lu0r38gWm6!21l")

    conn.runMQTT()
    #test.run()



