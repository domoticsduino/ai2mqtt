# ai2mqtt.py
import logging
import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import logging.config
from google import genai
from google.genai import types

_VERSION = "0.1"

load_dotenv()
with open('logging.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)
logger = logging.getLogger("ai2mqtt")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "ai2mqtt")
MQTT_2AI_TOPIC = os.getenv("MQTT_2AI_TOPIC", "ai2mqtt/prompt")
MQTT_FROMAI_TOPIC = os.getenv("MQTT_FROMAI_TOPIC", "ai2mqtt/response")

genai_config = types.GenerateContentConfig(
    response_mime_type="application/json",
)

clientAI = genai.Client()

def on_connect(client, userdata, flags, rc, properties=None):
    logger.info(f"MQTT connection successfully ({rc})")
    if MQTT_2AI_TOPIC:
        client.subscribe(f"{MQTT_2AI_TOPIC}")

def on_message(client, userdata, msg):
    try:
        logger.info(f"topic received: {msg.topic}")
        topic = f"{MQTT_FROMAI_TOPIC}"
        payload = json.loads(msg.payload.decode('utf-8').lower())
        logger.info(f"Payload: {payload}")
        if "track" in payload:
            topic = topic + f"/{payload['track']}"
            if "prompt" in payload and "scheme" in payload:                
                genai_config.response_schema = json.loads(payload["scheme"])
                response = clientAI.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[payload["prompt"]],
                    config=genai_config
                )
                output = json.loads(response.text)
                if output is not None:
                    logger.info(f"Response: {output}")            
                    client.publish(topic, json.dumps({"error": False, "response": output}))
                else:
                    raise ValueError("Invalid response")
            else:
                raise ValueError("Missing prompt or scheme")
        else:
            raise ValueError("Missing track")
    except Exception as e:
        logger.error(f"Error: {e}")
        client.publish(topic, json.dumps({"error": True, "error_message": str(e)}))

def print_initial_info():
    logger.info(f"START version {_VERSION}")
    logger.debug(f"MQTT_BROKER: {MQTT_BROKER}")
    logger.debug(f"MQTT_PORT: {MQTT_PORT}")
    logger.debug(f"MQTT_USERNAME: {MQTT_USERNAME}")
    logger.debug(f"MQTT_CLIENT_ID: {MQTT_CLIENT_ID}")
    logger.debug(f"MQTT_2AI_TOPIC: {MQTT_2AI_TOPIC}")
    logger.debug(f"MQTT_FROMAI_TOPIC: {MQTT_FROMAI_TOPIC}")
    
if __name__ == "__main__":

    print_initial_info()
    
    # MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    logger.info(f"MQTT_BROKER: {MQTT_BROKER}")
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logger.error(f"MQTT Connection error: {e}")
        exit()
    
    logger.info("Waiting for messages...")
    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logger.error("Subscriber disconnected.")
    finally:
        mqtt_client.disconnect()
        logger.error("Subscriber disconnected.")
