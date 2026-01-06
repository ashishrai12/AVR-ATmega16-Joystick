# API Documentation

This document provides detailed API documentation for all modules in the AVR-ATmega16-Joystick library.

---

## Table of Contents

1. [ADC Module](#adc-module)
2. [LCD Module](#lcd-module)
3. [Joystick Module](#joystick-module)
4. [Configuration](#configuration)

---

## ADC Module

**Header:** `include/adc.h`  
**Source:** `src/adc.c`

The ADC module provides functions for interfacing with the Analog-to-Digital Converter on AVR ATmega16/ATmega32 microcontrollers.

### Functions

#### `void adc_init(void)`

Initialize the ADC peripheral.

**Configuration:**
- Reference: AVCC with external capacitor
- Left-adjusted result for 8-bit mode
- Prescaler: 128 (for 125kHz ADC clock at 16MHz CPU)

**Example:**
```c
#include "adc.h"

int main(void) {
    adc_init();
    // ADC is now ready to use
}
```

---

#### `uint16_t adc_read(uint8_t channel)`

Read a 10-bit ADC value from the specified channel.

**Parameters:**
- `channel` - ADC channel to read (0-7)

**Returns:**
- 10-bit ADC value (0-1023)

**Example:**
```c
uint16_t x_value = adc_read(0);  // Read channel 0 (X-axis)
int16_t centered = x_value - 512; // Center around 0
```

---

#### `uint8_t adc_read_8bit(uint8_t channel)`

Read an 8-bit ADC value from the specified channel.

Uses left-adjusted mode for faster 8-bit readings.

**Parameters:**
- `channel` - ADC channel to read (0-7)

**Returns:**
- 8-bit ADC value (0-255)

**Example:**
```c
uint8_t x = adc_read_8bit(0);  // Fast 8-bit read
uint8_t y = adc_read_8bit(1);
```

---

#### `uint8_t adc_to_percent(uint8_t value)`

Convert an 8-bit ADC value to a percentage.

**Parameters:**
- `value` - 8-bit ADC value (0-255)

**Returns:**
- Percentage (0-100)

**Example:**
```c
uint8_t raw = adc_read_8bit(0);
uint8_t percent = adc_to_percent(raw);  // 0-100%
```

---

## LCD Module

**Header:** `include/lcd.h`  
**Source:** `src/lcd.c`

The LCD module provides functions for controlling HD44780-compatible 16x2 character LCD displays in 8-bit mode.

### Pin Configuration

| LCD Pin | MCU Pin | Description |
|---------|---------|-------------|
| RS      | PB0     | Register Select |
| RW      | PB1     | Read/Write |
| E       | PB2     | Enable |
| D0-D7   | PC0-PC7 | Data Bus |

### Functions

#### `void lcd_init(void)`

Initialize the LCD display.

**Configuration:**
- 8-bit interface mode
- 2-line display
- 5x7 character font
- Display on, cursor on

**Example:**
```c
#include "lcd.h"

int main(void) {
    lcd_init();
    lcd_print("Hello World!");
}
```

---

#### `void lcd_command(uint8_t cmd)`

Send a command byte to the LCD.

**Parameters:**
- `cmd` - Command byte

**Common Commands:**
| Command | Value | Description |
|---------|-------|-------------|
| Clear   | 0x01  | Clear display |
| Home    | 0x02  | Return home |
| Line 1  | 0x80  | Set cursor to line 1 |
| Line 2  | 0xC0  | Set cursor to line 2 |

---

#### `void lcd_data(uint8_t data)`

Send a data byte (character) to the LCD.

**Parameters:**
- `data` - Character to display

---

#### `void lcd_clear(void)`

Clear the display and return cursor to home position.

---

#### `void lcd_set_cursor(uint8_t row, uint8_t col)`

Set the cursor position.

**Parameters:**
- `row` - Row number (0 or 1)
- `col` - Column number (0-15)

**Example:**
```c
lcd_set_cursor(1, 5);  // Move to row 1, column 5
lcd_print("X=128");
```

---

#### `void lcd_print(const char *str)`

Print a null-terminated string at the current cursor position.

**Parameters:**
- `str` - String to print

---

#### `void lcd_putc(char c)`

Print a single character at the current cursor position.

**Parameters:**
- `c` - Character to print

---

#### `void lcd_print_int(int16_t value)`

Print an integer value at the current cursor position.

**Parameters:**
- `value` - Integer to print (-32768 to 32767)

**Example:**
```c
int16_t x = 128;
lcd_print("X=");
lcd_print_int(x);  // Displays "X=128"
```

---

## Joystick Module

**Header:** `include/joystick.h`  
**Source:** `src/joystick.c`

The Joystick module provides functions for reading analog joystick position and detecting direction.

### Types

#### `joystick_direction_t`

Enumeration of possible joystick directions.

```c
typedef enum {
    DIR_CENTER = 0,     // Joystick at rest
    DIR_NORTH,          // Up
    DIR_SOUTH,          // Down
    DIR_EAST,           // Right
    DIR_WEST,           // Left
    DIR_NORTH_EAST,     // Up-Right
    DIR_NORTH_WEST,     // Up-Left
    DIR_SOUTH_EAST,     // Down-Right
    DIR_SOUTH_WEST      // Down-Left
} joystick_direction_t;
```

#### `joystick_position_t`

Structure for holding joystick X/Y position.

```c
typedef struct {
    uint8_t x;  // X-axis value (0-255)
    uint8_t y;  // Y-axis value (0-255)
} joystick_position_t;
```

### Functions

#### `void joystick_init(void)`

Initialize the joystick interface (configures ADC).

---

#### `void joystick_read(joystick_position_t *pos)`

Read the current joystick position.

**Parameters:**
- `pos` - Pointer to structure to store position

**Example:**
```c
joystick_position_t pos;
joystick_read(&pos);
// pos.x and pos.y now contain joystick position
```

---

#### `uint8_t joystick_get_x(void)`

Get the current X-axis value.

**Returns:**
- X-axis ADC value (0-255)

---

#### `uint8_t joystick_get_y(void)`

Get the current Y-axis value.

**Returns:**
- Y-axis ADC value (0-255)

---

#### `joystick_direction_t joystick_get_direction(uint8_t x, uint8_t y)`

Determine direction from X/Y values.

Uses threshold-based zone detection:

```
     Y=255 (North)
        ↑
        |
X=0 ←---+---→ X=255
(West)  |    (East)
        ↓
     Y=0 (South)
```

**Parameters:**
- `x` - X-axis value (0-255)
- `y` - Y-axis value (0-255)

**Returns:**
- Detected direction

**Example:**
```c
uint8_t x = joystick_get_x();
uint8_t y = joystick_get_y();
joystick_direction_t dir = joystick_get_direction(x, y);

if (dir == DIR_NORTH) {
    // Joystick pushed up
}
```

---

#### `const char* joystick_direction_to_string(joystick_direction_t dir)`

Convert direction enum to a string.

**Parameters:**
- `dir` - Direction enumeration value

**Returns:**
- String representation ("N", "S", "E", "W", "NE", "NW", "SE", "SW", "C")

**Example:**
```c
joystick_direction_t dir = joystick_get_direction(x, y);
lcd_print(joystick_direction_to_string(dir));  // Prints "N", "SE", etc.
```

---

#### `uint8_t joystick_is_centered(uint8_t x, uint8_t y)`

Check if the joystick is in the center (dead) zone.

**Parameters:**
- `x` - X-axis value (0-255)
- `y` - Y-axis value (0-255)

**Returns:**
- 1 if in center zone, 0 otherwise

---

## Configuration

**Header:** `include/config.h`

Central configuration file containing all hardware settings and thresholds.

### CPU Configuration

```c
#define F_CPU 16000000UL  // 16 MHz CPU frequency
```

### ADC Configuration

```c
#define JOYSTICK_X_CHANNEL  0   // X-axis on ADC0
#define JOYSTICK_Y_CHANNEL  1   // Y-axis on ADC1
#define ADC_MIN             0
#define ADC_MAX             255
#define ADC_CENTER          128
```

### Direction Thresholds

```c
// Cardinal directions
#define THRESHOLD_NORTH_Y   240
#define THRESHOLD_SOUTH_Y   50
#define THRESHOLD_EAST_X    240
#define THRESHOLD_WEST_X    70

// Center (dead) zone
#define CENTER_X_MIN        70
#define CENTER_X_MAX        180
#define CENTER_Y_MIN        110
#define CENTER_Y_MAX        160

// Diagonal detection
#define DIAGONAL_THRESHOLD_HIGH  230
#define DIAGONAL_THRESHOLD_LOW   50
```

### LCD Pin Configuration

```c
#define LCD_RS_PIN      PB0
#define LCD_RW_PIN      PB1
#define LCD_EN_PIN      PB2
#define LCD_CTRL_PORT   PORTB
#define LCD_DATA_PORT   PORTC
```

---

## Usage Example

Complete example using all modules:

```c
#include <avr/io.h>
#include <util/delay.h>
#include "config.h"
#include "adc.h"
#include "lcd.h"
#include "joystick.h"

int main(void) {
    joystick_position_t pos;
    joystick_direction_t dir;
    
    // Initialize all peripherals
    joystick_init();
    lcd_init();
    
    // Display header
    lcd_print("Dir:");
    
    while (1) {
        // Read joystick
        joystick_read(&pos);
        dir = joystick_get_direction(pos.x, pos.y);
        
        // Update display
        lcd_set_cursor(0, 4);
        lcd_print("   ");  // Clear old value
        lcd_set_cursor(0, 4);
        lcd_print(joystick_direction_to_string(dir));
        
        // Show coordinates on line 2
        lcd_set_cursor(1, 0);
        lcd_print("X=");
        lcd_print_int(pos.x);
        lcd_print(" Y=");
        lcd_print_int(pos.y);
        
        _delay_ms(100);
    }
    
    return 0;
}
```
