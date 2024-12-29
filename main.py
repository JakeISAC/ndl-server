from core.face_detection import FaceDetection
from mqtt.mqtt import MQTTServer

if __name__ == '__main__':
    # start the MQTT messaging server
    mqtt = MQTTServer()
    mqtt.run()
    # start face detection daemon
    face_detection = FaceDetection(mqtt)
    face_detection.start()

