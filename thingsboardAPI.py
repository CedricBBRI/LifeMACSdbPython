import paho.mqtt.client as mqtt
import time

# Your Thingsboard host and access token
THINGSBOARD_HOST = 'digitalconstructionhub.ovh'
ACCESS_TOKEN = 'FclHfeTR9kReE6ZwPPYA'

# Initialize the MQTT client
client = mqtt.Client()

# Set the username for the MQTT client (in this case, the access token)
client.username_pw_set(ACCESS_TOKEN)


# Define a callback function that will be called when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("connected OK Returned code = ", rc)

        # Here you should subscribe to the topics of your sensors
        # Replace 'sensor/topic' with the topic of your sensor
        # If you want to subscribe to multiple topics, you can add more subscribe calls
        client.subscribe("v1/devices/ch1_fbg15/telemetry")
    else:
        print("Bad connection Returned code = ", rc)


# Define a callback function that will be called when a message is received from the server.
def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection: {rc}")


# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Make a connection to the MQTT broker
# Note: The port number 1884 is for secure MQTT connections. If you're not using secure MQTT, the default port number is 1883.
rconn = client.connect(THINGSBOARD_HOST, 1884, 60)

# Print the result of the connection attempt
print("server connection: ", mqtt.connack_string(rconn))

# Start the MQTT client loop
client.loop_start()

# Sleep for a certain period to allow time for the connection to establish and messages to arrive
# You can adjust the sleep duration as needed
time.sleep(100)