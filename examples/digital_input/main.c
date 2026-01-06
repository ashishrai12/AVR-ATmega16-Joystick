/**
 * @file main.c
 * @brief Digital Joystick Input Example
 * 
 * This example demonstrates reading digital joystick signals using
 * GPIO pins. The joystick switch outputs are read directly without ADC.
 * 
 * @note Original file: joystick_1.c
 * 
 * Hardware Setup:
 * - Joystick digital outputs connected to PORTD (pins 0-3)
 * - LED indicators on PORTD (pins 4-7)
 * 
 * @author Original Author
 * @date Refactored 2026
 */

#ifndef F_CPU
#define F_CPU 1000000UL  /**< 1 MHz CPU frequency */
#endif

#include <avr/io.h>
#include <util/delay.h>

/**
 * @brief Main entry point
 * 
 * Continuously monitors joystick digital input on PD1 and
 * controls LED indicators on PD4 and PD6.
 */
int main(void)
{
    /* Configure PORTD:
     * - Pins 0-3: Input mode (joystick signals)
     * - Pins 4-7: Output mode (LED indicators)
     */
    DDRD = 0xF0;
    
    /* Enable pull-ups on input pins */
    PORTD = 0x0F;
    
    while (1) {
        /* Clear LED outputs initially */
        PORTD &= ~(1 << PD4);
        PORTD &= ~(1 << PD6);
        
        /* Check joystick input on PD1 */
        if (~PIND & (1 << PD1)) {
            /* Button pressed (active low) - turn on LED on PD4 */
            PORTD |= (1 << PD4);
        }
        
        if (PIND & (1 << PD1)) {
            /* Button released - turn on LED on PD6 */
            PORTD |= (1 << PD6);
        } else {
            /* Default state - all LEDs off */
            PORTD &= ~(1 << PD4);
            PORTD &= ~(1 << PD6);
        }
    }
    
    return 0;
}
