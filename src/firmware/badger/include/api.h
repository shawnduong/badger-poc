#ifndef API_H
#define API_H

#include <ArduinoJson.h>  // ArduinoJson library by Benoit Blanchon.
#include <ESP8266HTTPClient.h>

uint16_t httpCode;
String httpResponse;

DynamicJsonDocument doc(1024);

/* POST JSON data to a host+path with an identity and write the output to a code, response. */
void post(String host, String path, uint64_t identity, uint16_t *code, String *response, String data)
{
	WiFiClient client;
	HTTPClient http;
	String url = host + path + "?identity=" + String(identity);

	http.begin(client, url);
	http.addHeader("Content-Type", "application/json");
	*code = http.POST(data);
	*response = http.getString();
	http.end();
}

/* Identify self to the online API. The status LED will light up blue while
   attempting, then green after being identified. */
void identify()
{
	Serial.println("Attempting to identify device with API.");
	led_rgb_blue();

	while (true)
	{
		post(API, "/api/badger/identify", IDENTITY, &httpCode, &httpResponse, "");
		if (httpCode == 200)  break;
		delay(5000);
	}

	Serial.println("Device identified.");
	led_clear(); led_rgb_green(); delay(1000); led_clear();
}

/* Ping to confirm device is still alive. It is not crucial this succeeds. */
void ping()
{
	post(API, "/api/badger/identify", IDENTITY, &httpCode, &httpResponse, "");
}

/* Send a card ID to the API. Return 0 if invalid, 1 if valid, 2 if on cooldown,
   or 3 if the reader is unauthorized. If max attempts have been reached without
   a 200 response, return -1. */
int8_t scan(uint8_t attempts, uint32_t id)
{
	for (uint8_t i = 0; i < attempts; i++)
	{
		post(API, "/api/badger/scan", IDENTITY, &httpCode, &httpResponse,
			"{\"id\":"+String(id)+"}");

		if (httpCode == 200)
		{
			deserializeJson(doc, httpResponse);
			return doc["rcode"];
		}

		delay(1000);
	}

	return -1;
}

#endif
