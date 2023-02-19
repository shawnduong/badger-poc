#include "config.h"
#include "include/rc522.h"
#include "include/sn74hc595n.h"
#include "include/led.h"
#include "include/networking.h"
#include "include/diag.h"

void setup()
{
	Serial.begin(9600);
	rc522_init();
	shift_init();
	post();
}

void loop()
{
	delay(100);
}
