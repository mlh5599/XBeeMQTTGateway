# import paho.mqtt.client as mqtt
# import logging

# client = mqtt.Client()


# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     logging.debug("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     # client.subscribe("$SYS/#")


# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     logging.debug(msg.topic+" "+str(msg.payload))


# def connect(mqtt_broker, port):

#     client.on_connect = on_connect
#     client.on_message = on_message

#     client.connect(mqtt_broker, port, 60)

#     client.topic_callback("test", on_message)

#     # Blocking call that processes network traffic, dispatches callbacks and
#     # handles reconnecting.
#     # Other loop*() functions are available that give a threaded interface and
#     # a manual interface.
#     client.loop_start()
