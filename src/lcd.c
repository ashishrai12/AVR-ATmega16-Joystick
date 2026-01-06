/**
 * @file lcd.c
 * @brief LCD Driver Implementation for HD44780-compatible displays
 */

#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include "../include/config.h"
#include "../include/lcd.h"

/**
 * @brief Generate enable pulse for LCD
 */
static void lcd_enable_pulse(void)
{
    LCD_CTRL_PORT |= (1 << LCD_EN_PIN);
    _delay_ms(LCD_ENABLE_PULSE_MS);
    LCD_CTRL_PORT &= ~(1 << LCD_EN_PIN);
    _delay_ms(LCD_ENABLE_PULSE_MS);
}

void lcd_command(uint8_t cmd)
{
    /* RS = 0 for command, RW = 0 for write */
    LCD_CTRL_PORT &= ~(1 << LCD_RS_PIN);
    LCD_CTRL_PORT &= ~(1 << LCD_RW_PIN);
    
    /* Put command on data port */
    LCD_DATA_PORT = cmd;
    
    /* Pulse enable */
    lcd_enable_pulse();
    
    _delay_ms(LCD_COMMAND_DELAY_MS);
}

void lcd_data(uint8_t data)
{
    /* RS = 1 for data, RW = 0 for write */
    LCD_CTRL_PORT |= (1 << LCD_RS_PIN);
    LCD_CTRL_PORT &= ~(1 << LCD_RW_PIN);
    
    /* Put data on data port */
    LCD_DATA_PORT = data;
    
    /* Pulse enable */
    lcd_enable_pulse();
    
    _delay_ms(LCD_COMMAND_DELAY_MS);
}

void lcd_init(void)
{
    /* Configure control pins as outputs */
    LCD_CTRL_DDR |= (1 << LCD_RS_PIN) | (1 << LCD_RW_PIN) | (1 << LCD_EN_PIN);
    
    /* Configure data port as output */
    LCD_DATA_DDR = 0xFF;
    
    /* Wait for LCD to power up */
    _delay_ms(50);
    
    /* Initialize LCD: Function Set (8-bit, 2 lines, 5x7) */
    lcd_command(LCD_CMD_FUNCTION_SET);
    _delay_ms(LCD_COMMAND_DELAY_MS);
    
    /* Display ON, Cursor ON */
    lcd_command(LCD_CMD_DISPLAY_ON);
    _delay_ms(LCD_COMMAND_DELAY_MS);
    
    /* Clear Display */
    lcd_command(LCD_CMD_CLEAR);
    _delay_ms(LCD_COMMAND_DELAY_MS);
    
    /* Entry Mode: Increment cursor, no shift */
    lcd_command(LCD_CMD_ENTRY_MODE);
    _delay_ms(LCD_COMMAND_DELAY_MS);
    
    /* Set cursor to home position */
    lcd_command(LCD_CMD_LINE1);
}

void lcd_clear(void)
{
    lcd_command(LCD_CMD_CLEAR);
    _delay_ms(2);  /* Clear command needs extra delay */
}

void lcd_set_cursor(uint8_t row, uint8_t col)
{
    uint8_t address;
    
    if (row == 0) {
        address = LCD_CMD_LINE1 + col;
    } else {
        address = LCD_CMD_LINE2 + col;
    }
    
    lcd_command(address);
}

void lcd_print(const char *str)
{
    while (*str) {
        lcd_data(*str++);
    }
}

void lcd_putc(char c)
{
    lcd_data(c);
}

void lcd_print_int(int16_t value)
{
    char buffer[7];  /* Enough for -32768 + null */
    itoa(value, buffer, 10);
    lcd_print(buffer);
}
