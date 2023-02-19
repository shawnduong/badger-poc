#include "config.h"
#include "include/rc522.h"
#include "include/sn74hc595n.h"
#include "include/led.h"
#include "include/networking.h"
#include "include/diag.h"
#include "include/api.h"

void setup()
{
	Serial.begin(9600);

	/* Initialization and self-test. */
	rc522_init();
	shift_init();
	post();

	/* Identify the unit to the API. */
	identify(API, "/api/badger/identify", IDENTITY);
}

void loop()
{
	delay(100);
}
