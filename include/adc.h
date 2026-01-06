/**
 * @file adc.h
 * @brief ADC Driver Interface for AVR ATmega16/ATmega32
 * 
 * This module provides functions for initializing and reading from the
 * Analog-to-Digital Converter peripherals.
 */

#ifndef ADC_H
#define ADC_H

#include <stdint.h>

/**
 * @brief Initialize the ADC peripheral
 * 
 * Configures the ADC with:
 * - AVCC as reference voltage
 * - ADC prescaler for optimal sampling rate
 * - Left-adjusted result for 8-bit readings
 */
void adc_init(void);

/**
 * @brief Read 10-bit ADC value from specified channel
 * 
 * @param channel ADC channel to read (0-7 for ATmega16/32)
 * @return uint16_t 10-bit ADC result (0-1023)
 */
uint16_t adc_read(uint8_t channel);

/**
 * @brief Read 8-bit ADC value from specified channel
 * 
 * Uses left-adjusted mode for faster 8-bit readings.
 * 
 * @param channel ADC channel to read (0-7 for ATmega16/32)
 * @return uint8_t 8-bit ADC result (0-255)
 */
uint8_t adc_read_8bit(uint8_t channel);

/**
 * @brief Convert raw ADC value to percentage
 * 
 * @param value Raw ADC value (0-255 for 8-bit)
 * @return uint8_t Percentage (0-100)
 */
uint8_t adc_to_percent(uint8_t value);

#endif /* ADC_H */
