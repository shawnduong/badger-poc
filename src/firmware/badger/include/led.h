#ifndef LED_H
#define LED_H

byte bits = 0b0000000;

void led_clear()
{
	bits = 0b0000000;
	shift_out(bits);
}

void led_blue()
{
	bits |= 0b010000;
	shift_out(bits);
}

void led_green()
{
	bits |= 0b100000;
	shift_out(bits);
}

void led_rgb_red()
{
	bits |= 0b000010;
	shift_out(bits);
}

void led_rgb_green()
{
	bits |= 0b000100;
	shift_out(bits);
}

void led_rgb_blue()
{
	bits |= 0b001000;
	shift_out(bits);
}

#endif
