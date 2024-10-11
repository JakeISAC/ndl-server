import paho.mqtt.client as mqtt
import time
import threading


class MQTTServer:
    def __init__(self):
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "localhost"
        self._port = 1883
        self._topic = "test/topic"
        self._client = mqtt.Client("Server")
        # connect to the MQTT server on class init
        self._connect()

    def _connect(self):
        self._client.connect(self._broker, self._port)

    def _mqtt_loop(self):
        self._client.loop_start()

    def send_message(self, message, topic=None):
        if not topic:
            topic = self._topic
        self._client.publish(topic, message)
        print(f"Published: {message}")

    def run(self):
        mqtt_thread = threading.Thread(target=self._mqtt_loop)
        mqtt_thread.start()
        try:
            while True:
                self.send_message("Hello from the publisher")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Publisher stopped")
        self._client.loop_stop()
        self._client.disconnect()
        mqtt_thread.join()
