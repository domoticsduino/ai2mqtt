# ai2mqtt

This Python script acts as a bridge between **GEMINI AI Engine** and the **MQTT protocol**.

It allows you to seamlessly integrate informations obtained from AI into your existing smart home ecosystem that supports MQTT, like OpenHAB.

Designed for ease of deployment, this solution can be run natively or as a Docker container, providing a portable and consistent environment.

Using the prompts received from external systems, it is able to provide the answers obtained by AI on a particular MQTT topic. This way the calling system does not have to be technically capable of interfacing with the AI ​​engine.

Tested with **GEMINI AI 2.5-flash model**

## Usage

- Copy *.env-template* in *.env* and populate config variables according to your setup (see .env.example for help)
- Make the appropriate changes to the logging.json file for management of application log
- Follow this guide to obtain your Gemini API KEY: https://ai.google.dev/gemini-api/docs/api-key
- Run ai2mqtt.py using your python environment OR run with docker compose
- Send prompts to *MQTT_2AI_TOPIC* topic and wait for the response on topic *MQTT_FROMAI_TOPIC*

### Payload template for prompt request

{"track": "[string_to_track_response]", "prompt": "[textual_prompt]", "schema": ["deserielized_json_schema_for_response"]}

*string_to_track_response* => the response will be sent to topic *MQTT_FROMAI_TOPIC/[track]*

*deserielized_json_schema_for_response* => AI will try to respond by populating the provided json schema (must be a deserialized json object)

Example:

Send the following payload to *MQTT_2AI_TOPIC* topic 

{
  "track": "weatherforecast",
  "prompt": "I need the weather forecast for New York at Christmas",
  "scheme": "{\\"title\\": \\"WeatherforecastResponse\\", \\"type\\": \\"object\\", \\"description\\": \\"scheme for obtaining weather forecasts\\", \\"properties\\": {\\"location\\": {\\"type\\": \\"string\\", \\"description\\": \\"the location used for forecasts\\"}, \\"condition\\": {\\"type\\": \\"string\\", \\"description\\": \\"the textual description of the weather forecast\\"}}, \\"required\\": [\\"location\\", \\"condition\\"]}"
}

Response will be trasmitted to *MQTT_FROMAI_TOPIC*/weatherforecast topic using the provided schema

### Response template

Response will be sent using the following json template

{
  "error": [*true/false*],
  "error_message": [*string, only in case of errors*],
  "response": [*json schema filled with AI response, only in case of successfull response*]
}

### Environment configuration

- *MQTT_BROKER*=**mqtt broker ip address**
- *MQTT_PORT*=**mqtt broker port**
- *MQTT_USERNAME*=**mqtt broker username (if needed)**
- *MQTT_PASSWORD*=**mqtt broker password (if needed)**
- *MQTT_CLIENT_ID*=**mqtt_client_id**
- *MQTT_2AI_TOPIC*=**topic to use for sending prompts from external systems**
- *MQTT_FROMAI_TOPIC*=**topic to use for receiving responses**
- *GEMINI_API_KEY*=**gemini api key** see https://ai.google.dev/gemini-api/docs/api-key

### MQTT Topics

- *MQTT_2AI_TOPIC*=**to send prompt to AI**
- *MQTT_FROMAI_TOPIC/[track]*=**to receive prompt response from AI**

## Resources
 - Youtube videos: https://youtube.com/playlist?list=PLvTDReD06z45jwp9Kakuw0TTBLnL_DkVK&si=TCcI4w81hZxVe9CK

## *Version 1.0 beta*
 - Final version

## *Version 0.1*
 - Initial version

# DISCLAIMER

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.