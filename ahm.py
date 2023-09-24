import paho.mqtt.client as mqtt
import json
import requests

# MQTT Broker Details
mqtt_broker_host = "127.0.0.1"
mqtt_broker_port = 1883


# AWS API Endpoint
aws_api_endpoint = "https://no1n1k6iq8.execute-api.us-east-1.amazonaws.com/default/Rekog_Meraki"

# Callback when MQTT message is received
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    if "objects" in payload and len(payload["objects"]) > 0:
        detected_object = payload["objects"][0]
        if detected_object.get("type") == "person":
            # Invoke the AWS API
                print("A Person Has been Detected by MV")
            response = requests.get(aws_api_endpoint)
            if response.status_code == 200:
                print("AWS API invoked successfully")
            else:
                print(f"Failed to invoke AWS API. Status code: {response.status_code}")

# Create an MQTT client
client = mqtt.Client()
#client.username_pw_set(mqtt_username, mqtt_password)

# Set the callback function for when a message is received
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker_host, mqtt_broker_port, 60)

# Subscribe to the Meraki Camera topic
camera_topic = "/merakimv/Q2HV-DCPL-VH2W/raw_detections"
client.subscribe(camera_topic)

# Start the MQTT loop to listen for messages
client.loop_forever()