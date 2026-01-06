/**
 * @file main.c
 * @brief Direction Display Example - Shows Cardinal/Diagonal Directions on LCD
 * 
 * This example demonstrates reading joystick position and displaying
 * the detected direction (N, S, E, W, NE, NW, SE, SW, C) on an LCD.
 * 
 * @note Original file: Joystick_3_Directions.c
 * 
 * Hardware Setup:
 * - Joystick X-axis connected to ADC channel 0 (PA0)
 * - Joystick Y-axis connected to ADC channel 1 (PA1)
 * - LCD data bus connected to PORTC
 * - LCD control pins (RS, RW, EN) connected to PORTB (PB0, PB1, PB2)
 * 
 * @author Original Author
 * @date Refactored 2026
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "../../include/config.h"
#include "../../include/adc.h"
#include "../../include/lcd.h"
#include "../../include/joystick.h"

/**
 * @brief Main entry point
 * 
 * Initializes the LCD and joystick, then continuously reads
 * joystick position and displays the detected direction.
 */
int main(void)
{
    joystick_position_t pos;
    joystick_direction_t dir;
    joystick_direction_t last_dir = DIR_CENTER;
    
    /* Configure LED port as output */
    LED_DDR = 0xFF;
    
    /* Enable global interrupts */
    sei();
    
    /* Initialize peripherals */
    joystick_init();
    lcd_init();
    
    /* Display startup message */
    lcd_print("Direction:");
    lcd_set_cursor(1, 0);
    lcd_print("C");
    
    _delay_ms(500);
    
    while (1) {
        /* Read joystick position */
        joystick_read(&pos);
        
        /* Determine direction */
        dir = joystick_get_direction(pos.x, pos.y);
        
        /* Only update display if direction changed */
        if (dir != last_dir) {
            /* Clear direction area on line 2 */
            lcd_set_cursor(1, 0);
            lcd_print("   ");  /* Clear 3 characters */
            
            /* Display new direction */
            lcd_set_cursor(1, 0);
            lcd_print(joystick_direction_to_string(dir));
            
            last_dir = dir;
        }
        
        /* Small delay to debounce */
        _delay_ms(100);
    }
    
    return 0;
}

/**
 * @brief ADC Conversion Complete Interrupt
 * 
 * Triggered when ADC conversion completes. Starts the next conversion.
 */
ISR(ADC_vect)
{
    ADCSRA |= (1 << ADSC);  /* Start next conversion */
}
