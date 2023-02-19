#ifndef SN74HC595N_H
#define SN74HC595N_H

#define CLOCK 5 // D1
#define LATCH 0 // D3
#define DATAS 2 // D4

void shift_init()
{
	pinMode(CLOCK, OUTPUT); 
	pinMode(LATCH, OUTPUT); 
	pinMode(DATAS, OUTPUT); 
}

void shift_out(byte b)
{
	digitalWrite(LATCH, LOW);
	shiftOut(DATAS, CLOCK, MSBFIRST, b);
	digitalWrite(LATCH, HIGH);
}

#endif
