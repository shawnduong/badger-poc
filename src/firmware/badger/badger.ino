#include "config.h"
#include "include/rc522.h"
#include "include/sn74hc595n.h"
#include "include/led.h"
#include "include/networking.h"
#include "include/diag.h"
#include "include/api.h"

/* Time needed to pass with no activity before sleeping. */
#define TTS 20000  // ms

/* Sleep duration before waking to poll. */
#define SLEEP_DURATION 5e6  // us

int64_t ti;
int64_t tts;

byte idbuffer[12];
uint64_t id;
byte len;

void setup()
{
	Serial.begin(9600);

	/* Initialization and self-test. */
	rc522_init();
	shift_init();
	post();

	/* Identify the unit to the API. */
	identify();
}

void loop()
{
	ti = millis();

	/* Loop always starts in active state. */
	tts = TTS;
	led_rgb_white();

	/* Active. */
	while (tts > 0)
	{
		/* Go through active loop again if no ID read. */
		if (!read_uid(255, idbuffer, &len))
		{
			tts -= millis() - ti;
			continue;
		}

		/* Load the 4-byte ID (7-byte currently unsupported). */
		id = (idbuffer[0] << 0x18) | (idbuffer[1] << 0x10) | (idbuffer[2] << 0x08) | idbuffer[3];

		/* Send the ID to the API. */
		switch (scan(4, id))
		{
			case -1:
				led_clear();
				led_rgb_red();
				led_blue();
				break;
			case 0:
				led_clear();
				led_rgb_red();
				break;
			case 1:
				led_green();
				break;
			case 2:
				led_blue();
				break;
			case 3:
				led_clear();
				led_rgb_blue();
				led_blue();
				break;
			default:
				Serial.println("Unrecognized response from API.");
		}

		delay(1000); led_clear(); led_rgb_white();
	}

	led_clear();

	/* Inactive, sleeping mode. */
	while (true)
	{
		ESP.deepSleep(SLEEP_DURATION);
		led_blue();
		if (read_uid(16, idbuffer, &len))  break;
		led_clear();
	}
}
