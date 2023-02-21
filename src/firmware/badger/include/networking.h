#ifndef NETWORK_H
#define NETWORK_H

#include <ESP8266WiFi.h>
#include <WiFiClient.h>

#define POLL_INTERVAL 100  // ms

/* Connect to a Wi-Fi network using its SSID and password. If after timeout ms,
   Wi-Fi connection is unsuccessful, return false. */
bool connect(String ssid, String password, uint16_t timeout)
{
	WiFi.mode(WIFI_STA);
	WiFi.begin(ssid, password);

	for (uint8_t i = 0; i < timeout/POLL_INTERVAL; i++)
	{
		if (WiFi.status() == WL_CONNECTED)  return true;

		led_rgb_blue();
		delay(POLL_INTERVAL/2);
		led_clear();
		delay(POLL_INTERVAL/2);
	}

	return false;
}

/* Return true if connected to a Wi-Fi network. */
bool is_connected()
{
	return (WiFi.status() == WL_CONNECTED);
}

/* Get the MAC address of the ESP8266. */
String get_mac()
{
	return WiFi.macAddress();
}

/* Force Wi-Fi sleep for a duration given in ms. */
void radio_sleep(uint64_t duration)
{
	WiFi.forceSleepBegin();
	delay(duration);
	WiFi.forceSleepWake();
}

#endif
