/**
 * @file main.c
 * @brief X/Y Coordinate Display Example - Shows Raw Joystick Values on LCD
 * 
 * This example demonstrates reading joystick X and Y axis values
 * and displaying them as numeric coordinates on an LCD display.
 * 
 * @note Original file: Joystick_3_XY.c
 * 
 * Hardware Setup:
 * - Joystick X-axis connected to ADC channel 0 (PA0)
 * - Joystick Y-axis connected to ADC channel 1 (PA1)
 * - LCD data bus connected to PORTC
 * - LCD control pins (RS, RW, EN) connected to PORTB (PB0, PB1, PB2)
 * 
 * LCD Display Format:
 *   Line 1: "X=xxx Y=yyy"
 *   Line 2: (available for additional info)
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
 * @brief Display X and Y values on LCD
 * 
 * @param x X-axis value (0-255)
 * @param y Y-axis value (0-255)
 */
static void display_coordinates(uint8_t x, uint8_t y)
{
    /* Display X value */
    lcd_set_cursor(0, 0);
    lcd_print("X=");
    
    /* Clear previous X value area */
    lcd_print("   ");
    lcd_set_cursor(0, 2);
    lcd_print_int(x);
    
    /* Display Y value */
    lcd_set_cursor(0, 6);
    lcd_print("Y=");
    
    /* Clear previous Y value area */
    lcd_print("   ");
    lcd_set_cursor(0, 8);
    lcd_print_int(y);
}

/**
 * @brief Main entry point
 * 
 * Initializes the LCD and joystick, then continuously reads
 * and displays X/Y coordinate values.
 */
int main(void)
{
    joystick_position_t pos;
    
    /* Configure LED port as output */
    LED_DDR = 0xFF;
    
    /* Enable global interrupts */
    sei();
    
    /* Initialize peripherals */
    joystick_init();
    lcd_init();
    
    /* Display labels */
    lcd_print("X=    Y=");
    
    _delay_ms(100);
    
    while (1) {
        /* Read joystick position */
        joystick_read(&pos);
        
        /* Update display with new values */
        display_coordinates(pos.x, pos.y);
        
        /* Delay between readings */
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
