/**
 * @file adc.c
 * @brief ADC Driver Implementation for AVR ATmega16/ATmega32
 */

#include <avr/io.h>
#include <util/delay.h>
#include "../include/config.h"
#include "../include/adc.h"

void adc_init(void)
{
    /* Set ADC input pins as input (PORTA for ATmega16/32) */
    JOYSTICK_INPUT_DDR = 0x00;
    
    /* Configure ADMUX:
     * - REFS0 = 1: AVCC as reference voltage
     * - ADLAR = 1: Left-adjust result for 8-bit readings
     */
    ADMUX = (1 << REFS0) | (1 << ADLAR);
    
    /* Configure ADCSRA:
     * - ADEN = 1: Enable ADC
     * - ADPS[2:0] = 111: Prescaler = 128 (for 16MHz -> 125kHz ADC clock)
     */
    ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
}

uint16_t adc_read(uint8_t channel)
{
    /* Select channel (clear MUX bits, then set new channel) */
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
    
    /* Disable left-adjust for 10-bit reading */
    ADMUX &= ~(1 << ADLAR);
    
    /* Start conversion */
    ADCSRA |= (1 << ADSC);
    
    /* Wait for conversion to complete */
    while (ADCSRA & (1 << ADSC));
    
    /* Return 10-bit result */
    return ADC;
}

uint8_t adc_read_8bit(uint8_t channel)
{
    /* Select channel (clear MUX bits, then set new channel) */
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
    
    /* Enable left-adjust for 8-bit reading */
    ADMUX |= (1 << ADLAR);
    
    /* Start conversion */
    ADCSRA |= (1 << ADSC);
    
    /* Wait for conversion to complete */
    while (ADCSRA & (1 << ADSC));
    
    /* Return upper 8 bits (ADCH) */
    return ADCH;
}

uint8_t adc_to_percent(uint8_t value)
{
    /* Convert 0-255 to 0-100 */
    return (uint8_t)((uint16_t)value * 100 / 255);
}
