from MQTT import MqttSap
import random
from gui import Screen
from utils import Utils

#from MQTTv2 import MqttSap

if __name__ == '__main__':

    #mainScr = Screen().start()

    conn = MqttSap("62AF49DA78D94E18BDE93A64ED17DB28",
                   "./certificates/certificate_real.pem",
                   "!S3?OhPerZMy4I3IzN0tu?u3WwFkWEHVGvch")

    #Utils.loadData("C:\\Users\\erick.simas.grilo\\OneDrive - Accenture\\SAP PM\\Iniciativa IAM\\Template_migration_IAM.xlsx")

    conn.runMQTT("[BRA] Air conditioning","BRA_Air_conditioning",[[random.randint(1,60)]],None,True,True)

    #test.run()



