#ifndef LED_H
#define LED_H

void led_clear()
{
	shift_out(0b000000);
}

void led_blue()
{
	shift_out(0b010000);
}

void led_green()
{
	shift_out(0b100000);
}

void led_rgb_red()
{
	shift_out(0b000010);
}

void led_rgb_blue()
{
	shift_out(0b000100);
}

void led_rgb_green()
{
	shift_out(0b001000);
}

#endif
