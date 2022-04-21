from MQTT import MqttSap
#import test


if __name__ == '__main__':
    conn = MqttSap("68FFC2DD2E344280885511AD07E61A8",
                   "./certificates/certificate_real.pem")
    conn.runMQTT()
    #test.run()

