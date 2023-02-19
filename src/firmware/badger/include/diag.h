#ifndef DIAG_H
#define DIAG_H

void post()
{
	Serial.println("Running power on self test (POST).");

	/* Verify the shift register and all LEDs are working. */
	Serial.println("Running shift register test.");
	byte sequence[] = {0b111110, 0b000010, 0b000100, 0b001000, 0b010000, 0b100000, 0};

	for (byte i = 0; i < sizeof(sequence)/sizeof(sequence[0]); i++)
	{
		shift_out(sequence[i]);
		delay(500);
	}

	/* RC522 scanner test only needed during the production phase. */
	#ifdef QA
		Serial.println("Running RC522 test.");
		Serial.println("Please tap a card.");

		byte idbuffer[12];
		uint64_t id;
		byte len = 4;

		while (true)
		{
			if (!read_uid(255, idbuffer, &len))  continue;
			id = (idbuffer[0] << 0x18) | (idbuffer[1] << 0x10) | (idbuffer[2] << 0x08) | idbuffer[3];
			Serial.print("Read id: "); Serial.println(id);
			shift_out(0b100000);
			break;
		}
		led_green();
		delay(500);
		led_clear();

	#endif

	/* Network test for connectivity. */
	Serial.println("Running network test.");
	while (!connect(NET_SSID, NET_PASS, TIMEOUT));
	led_rgb_green(); delay(500); led_clear();

	Serial.println("POST complete.");
}

#endif
