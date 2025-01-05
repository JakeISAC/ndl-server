from core.face_detection import FaceDetection
from mqtt.mqtt import MQTTServer
from daemon.session_token_daemon import SessionTokenDaemon

if __name__ == '__main__':
    # start the MQTT messaging server
    mqtt = MQTTServer()
    mqtt.run()
    # start session token daemon
    session_daemon = SessionTokenDaemon()
    session_daemon.run()
    # start face detection daemon
    face_detection = FaceDetection(mqtt)
    face_detection.run()
