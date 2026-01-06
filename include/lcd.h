/**
 * @file lcd.h
 * @brief LCD Driver Interface for HD44780-compatible displays
 * 
 * This module provides functions for controlling a 16x2 character LCD
 * in 8-bit mode connected to an AVR ATmega16/ATmega32.
 */

#ifndef LCD_H
#define LCD_H

#include <stdint.h>

/**
 * @brief Initialize the LCD display
 * 
 * Configures GPIO pins and initializes the LCD with:
 * - 8-bit interface mode
 * - 2 line display
 * - 5x7 character font
 * - Display on, cursor on
 */
void lcd_init(void);

/**
 * @brief Send a command byte to the LCD
 * 
 * @param cmd Command byte to send
 */
void lcd_command(uint8_t cmd);

/**
 * @brief Send a data byte to the LCD
 * 
 * @param data Data byte (character) to display
 */
void lcd_data(uint8_t data);

/**
 * @brief Clear the LCD display
 * 
 * Clears all characters and returns cursor to home position.
 */
void lcd_clear(void);

/**
 * @brief Set cursor position on LCD
 * 
 * @param row Row number (0 or 1)
 * @param col Column number (0-15)
 */
void lcd_set_cursor(uint8_t row, uint8_t col);

/**
 * @brief Print a string to the LCD at current cursor position
 * 
 * @param str Null-terminated string to print
 */
void lcd_print(const char *str);

/**
 * @brief Print a character to the LCD at current cursor position
 * 
 * @param c Character to print
 */
void lcd_putc(char c);

/**
 * @brief Print an integer value to the LCD
 * 
 * @param value Integer value to print
 */
void lcd_print_int(int16_t value);

#endif /* LCD_H */
