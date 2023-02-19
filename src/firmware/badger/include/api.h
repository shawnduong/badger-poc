#ifndef API_H
#define API_H

#include <ArduinoJson.h>  // ArduinoJson library by Benoit Blanchon.
#include <ESP8266HTTPClient.h>

/* GET some host+path with an identity and write the output to code, response. */
void get(String host, String path, uint64_t identity, uint16_t *code, String *response)
{
	WiFiClient client;
	HTTPClient http;
	String url = host + path + "?identity=" + String(identity);

	http.begin(client, url);
	*code = http.GET();
	*response = http.getString();
	http.end();
}

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
void identify(String host, String endpoint, uint32_t identity)
{
	uint16_t code;
	String response;

	Serial.println("Attempting to identify device with API.");
	led_rgb_blue();

	while (true)
	{
		post(host, endpoint, identity, &code, &response, "");
		Serial.println(code);
		Serial.println(response);
		if (code == 200)  break;
		delay(5000);
	}

	Serial.println("Device identified.");
	led_clear(); led_rgb_green(); delay(1000); led_clear();
}

#endif
