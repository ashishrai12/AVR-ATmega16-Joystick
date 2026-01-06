/**
 * @file main.c
 * @brief Basic ADC Joystick Reading Example
 * 
 * This example demonstrates reading analog joystick values using
 * the ADC module. X and Y axis values are read and centered.
 * 
 * @note Original file: Joystick_2.c
 * 
 * Hardware Setup:
 * - Joystick X-axis connected to ADC channel 0 (PA0)
 * - Joystick Y-axis connected to ADC channel 1 (PA1)
 * 
 * @author Original Author
 * @date Refactored 2026
 */

#include <avr/io.h>
#include <util/delay.h>
#include "../../include/config.h"
#include "../../include/adc.h"

/**
 * @brief Main entry point
 * 
 * Continuously reads joystick X and Y values via ADC,
 * centers them around 0 (subtracts 512 from 10-bit reading),
 * and adds a delay between readings.
 */
int main(void)
{
    int16_t x, y;
    
    /* Initialize ADC peripheral */
    adc_init();
    
    while (1) {
        /* Read X and Y axis values (10-bit) */
        x = adc_read(JOYSTICK_X_CHANNEL);
        y = adc_read(JOYSTICK_Y_CHANNEL);
        
        /* Center values around 0 (512 is the midpoint for 10-bit ADC) */
        x = x - 512;
        y = y - 512;
        
        /* 
         * At this point:
         * x ranges from -512 (full left) to +511 (full right)
         * y ranges from -512 (full down) to +511 (full up)
         * 
         * These values can be used to control motors, servos,
         * or other devices requiring signed position input.
         */
        
        /* Delay between readings */
        _delay_ms(250);
    }
    
    return 0;
}
